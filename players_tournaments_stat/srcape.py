import requests
from bs4 import BeautifulSoup
import os
from time import sleep
import json
from random import randrange


def league_parser(file_id):
    leagues = {}
    with open(f'data_templates/leagues/league_{file_id}.html', 'r', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    league_name = soup.find(class_="h5 heading-component-title").text

    try:
        players_table = soup.find_all(class_="table-custom table-roster")[0].find_all("tr")
    except:
        print("Couldn't find this information")

    players_table = players_table[1:]
    players_list = []
    for player in players_table:
        player_ranking = player.find(class_="text-center").text
        player_img = player.find_all(class_="text-center")[1].find("img").get("data-src")
        player_name = player.find(class_="text-left w-50").text
        player_rating = player.find(class_="text-center w-25").text
        players_list.append({"Player ranking": player_ranking,"Player name": player_name, "Player img": player_img, "Player rating": player_rating})


    try:
        clubs_table = soup.find_all(class_="table-custom table-roster")[1].find_all("tr")
    except:
        print("Couldn't find this information")


    clubs_table = clubs_table[1:]
    clubs_list = []
    for club in clubs_table:
        club_name = club.find(class_="text-left").text
        club_link = "https://en.soccerwiki.org/"+club.find(class_="pt-0 pb-0 pr-0 pl-2 text-center").find("a").get("href")
        club_logo = club.find(class_="pt-0 pb-0 pr-0 pl-2 text-center").find("img").get("data-src")
        club_manager = club.find_all(class_="text-left")[1].text
        club_stadium = club.find_all(class_="text-left")[2].text
        club_location = club.find_all(class_="text-left")[3].text
        clubs_list.append({"Club name": club_name,"Club link": club_link, "Club logo": club_logo, "Club manager": club_manager, "Club stadium": club_stadium, "Club location": club_location})

    try:
        referee_table = soup.find_all(class_="table-custom table-roster")[2].find_all("tr")
    except:
        print("Couldn't find this information")


    referee_table = referee_table[1:]
    referee_list = []
    for referee in referee_table:
        referee_name = referee.find(class_="text-left").text
        referee_link = "https://en.soccerwiki.org/"+referee.find(class_="pt-0 pb-0 pr-0 pl-2 text-center").find("a").get("href")
        referee_photo = referee.find(class_="pt-0 pb-0 pr-0 pl-2 text-center").find("img").get("data-src")
        referee_nationality = referee.find_all(class_="text-left")[1].text.strip()
        referee_list.append({"Referee name": referee_name, "Referee link": referee_link, "Referee photo": referee_photo, "Referee nationality": referee_nationality})

    try:
        clubs_winners_table = soup.find_all(class_="table-custom table-roster")[3].find_all("tr")
    except:
        print("Couldn't find this information")


    clubs_winners_table = clubs_winners_table[1:]
    clubs_winners_list = []
    for club in clubs_winners_table:
        season = club.find(class_="text-center").text
        club_name = club.find(class_="text-left").text
        club_link = "https://en.soccerwiki.org/"+club.find(class_="p-1").find("a").get("href")
        club_logo = club.find(class_="p-1").find("img").get("data-src")
        clubs_winners_list.append({"Season": season, "Club name": club_name, "Club link": club_link, "Club logo": club_logo})

    leagues[league_name] = {"Top players for the last season": players_list, "League clubs": clubs_list, "Referees":referee_list, "League Winners": clubs_winners_list}

    return leagues



def cup_parser(file_id):
    cups = {}
    with open(f'data_templates/cups/cup_{file_id}.html', 'r', encoding="utf-8") as file:
        src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        cup_winners = soup.find(class_="table-custom table-roster").find_all("tr")
        cup_winners = cup_winners[1:]

        cup_name = soup.find(class_="h5 heading-component-title").text

        cup_stat = {}
        for club in cup_winners:
            season = club.find(class_="text-center").text
            club_name = club.find(class_="text-left").text
            club_link = "https://en.soccerwiki.org/" + club.find(class_="text-left").find("a").get("href")
            # club_logo = club.find(class_="p-1").find("img").get("data-src")
            cup_stat[season] = {"Club name": club_name, "Club link": club_link}

        cups[cup_name] = cup_stat 

    return cups



def scraper(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    req = requests.get(url, headers)

    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(req.text)

    with open('index.html', 'r', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    articles = soup.find_all('article', class_="post-classic")
    tournaments_links_list = ["https://en.soccerwiki.org/" + article.find("div", class_="post-classic-aside").find("a", class_="post-classic-figure").get("href") for article in articles ]
    tournaments_links_list = tournaments_links_list[:-6]

    cups_list = []
    leagues_list = []

    count = 1
    iteration = len(tournaments_links_list) - 1
    for tournament_link in tournaments_links_list:
        req = requests.get(tournament_link, headers)

        file_id = tournament_link.split('=')[1]
        
        if "leagueid" in tournament_link:
            with open(f'data_templates/leagues/league_{file_id}.html', 'w', encoding="utf-8") as file:
                file.write(req.text)

                leagues = league_parser(file_id)
                leagues_list.append(leagues)
        elif "cupid" in tournament_link:
            with open(f'data_templates/cups/cup_{file_id}.html', 'w', encoding="utf-8") as file:
                file.write(req.text)

                cups = cup_parser(file_id)
                cups_list.append(cups)   
        else:
            pass

        print(f"Iteration №{count}, {iteration} left..")

        iteration -= 1
        count += 1

        if iteration == -1:
            print("Scraping finished")

        sleep(randrange(1, 2))


    result_data = {"Cups": cups_list, "Leagues": leagues_list}



    with open("result/project_data.json", "a", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)
    

def main():
    scraper("https://en.soccerwiki.org/league.php")



if __name__ == "__main__":
    main()