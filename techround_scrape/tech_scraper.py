import requests
from bs4 import BeautifulSoup
import re
import json 
from time import sleep
from random import randrange


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    req = requests.get(url, headers)

    with open('index.html', 'w') as file:
        file.write(req.text)

    with open('index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    articles = soup.find(class_ = "entry-content").find_all("a")
    
    project_urls = [article.get("href") for article in articles]
    
    project_data_list = []
    count = 1
    iteration = len(project_urls) - 1
    for project_url in project_urls:
        req = requests.get(project_url, headers)
        project_name = project_url.split("/")[-2]

        with open(f"data/{project_name}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"data/{project_name}.html", "r", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        try:
            project_name = soup.find(class_="mt-2").text
        except:
            project_name = "Name not found"

        try:
            temp = soup.find(class_="bgimage").get("style")
            project_picture = re.search(r'url\((.*?)\)', temp).group(1)

        except:
            project_picture  = "Picture not found"


        try:
            temp = soup.find(class_="entry-content").find_all("ul")[1].find_all("li")
            project_description = ""
            for desc in temp:
                project_description += desc.text.strip()
        except:
            pass
            project_description = "Project description not found"


        project_data_list.append(
            {
                "Project name": project_name,
                "Picture": project_picture,
                "Short description": project_description,
            }
        )

        print(f"Iteration №{count}, {iteration} left..")

        iteration -= 1
        count += 1

        if iteration == -1:
            print("Scraping finished")

        sleep(randrange(1, 3))

    with open("result/project_data.json", "a", encoding="utf-8") as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)


def main():
    get_data("https://techround.co.uk/a-z-startup-profiles/")


if __name__ == "__main__":
    main()
