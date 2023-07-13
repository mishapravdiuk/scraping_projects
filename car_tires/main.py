import csv
import requests
from bs4 import BeautifulSoup
import os
import json

def link_scraper(url):
    tires_links_lst = []

    for i in range(1, 10):
        url = f"{url}{i}"
        req = requests.get(url)

        response = req.text
        soup = BeautifulSoup(response, "html.parser")

        tire_links = soup.find_all("a", class_="product-card__image-container dflex-center")

        for link in tire_links: tires_links_lst.append("https://shiny-diski.com.ua"+link.get("href"))

        
    return tires_links_lst

def profile_scraper():
    tires_links_lst = link_scraper("https://shiny-diski.com.ua/uk/tires?start=")

    # tires_links_lst = ["https://shiny-diski.com.ua/uk/debica-presto-uhp-2-225-45-r17-91y"]
    indx = 1
    item_info_dict = {}
    for link in tires_links_lst:
        req = requests.get(link)
        response = req.text
        soup = BeautifulSoup(response, "html.parser")
        name = soup.find("h1", class_="product__caption").text
        try:
            full_price = soup.find("span", class_="standard-price js-price-sorting").text
        except:
            continue
        try:
            full_price = soup.find("span", class_="price-without-sale").text
            disc_price = soup.find("span", class_="discount js-price-sorting").text
        except:
            disc_price = "No discount"
        try:
            reviews_amount = soup.find(class_="reviews-rating__value").text 
        except:
            reviews_amount = "No reviews"
        try:
            car_type = soup.find("img", class_="property-value-icon js-tooltip").get("alt")
        except:
            car_type = "No info"
        try:
            season = soup.find_all("img", class_="property-value-icon js-tooltip")[1].get("alt")
        except:
            season  = "No info"
        try:
            rating = soup.find("span", class_="rating__score js-average-rating__score hidden").text
        except:
            rating  = "No info"
        try:
            certified = soup.find("div", class_="product__certified dflex-center js-tooltip js-product__certified js-scroll-to-tab").get("data-tooltip-title")
        except:
            certified  = "No info"
        try:
            country = soup.find("span", class_="js-production-data__value product__country-name").text
        except:
            country  = "No info"
        try:
            prod_year = soup.find("div", class_="js-production-data__year product__production-year").text
        except:
            prod_year   = "No info"
        try:
            width = soup.find("div", class_="properties__prperty-value dflex-center").text
        except:
            width   = "No info"
        try:
            profile = soup.find_all("div", class_="properties__prperty-value dflex-center")[1].text
        except:
            profile   = "No info"
        try:
            diameter = soup.find_all("div", class_="properties__prperty-value dflex-center")[2].text
        except:
            diameter   = "No info"
        try:
            load_index = soup.find_all("div", class_="properties__prperty-value dflex-center")[4].text
        except:
            load_index   = "No info"
        try:
            speed_index = soup.find_all("div", class_="properties__prperty-value dflex-center")[5].text
        except:
            speed_index   = "No info"    
        

        if not os.path.exists("data"):
            os.makedirs("data")
        else:
            pass

        with open(f"data/result.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    name,
                    link,
                    full_price,
                    disc_price,
                    car_type, 
                    season,
                    rating, 
                    reviews_amount,
                    certified, 
                    country, 
                    prod_year, 
                    width, 
                    profile, 
                    diameter, 
                    load_index, 
                    speed_index, 
                )
            )


        item_info_dict[name] = ["Full price: " + full_price,"Discount price: " +disc_price, "Reviews: " +reviews_amount, car_type, season, "Rating: " + rating, certified, "Country: " + country, "Production year: " + prod_year, "Width: "+ width, "Profile: " + profile, "Diameter: "+ diameter, "Load index: " + load_index, "Speed index: " + speed_index]
        print(f"Link {indx} scraped... {round((indx/len(tires_links_lst))*100, 2)}/100%")
        indx += 1
        
    with open("data/result_data.json", "a", encoding="utf-8") as file:
        json.dump(item_info_dict, file, indent=4, ensure_ascii=False)




def main():
    profile_scraper()


if __name__ == "__main__":
    main()


