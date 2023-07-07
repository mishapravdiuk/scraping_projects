import requests
import os
import img2pdf


def get_data():

    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    for i in range(1, 49):
        url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
        req = requests.get(url, headers)
        response = req.content
        
        with open(f"media/{i}.jpg", "wb") as file:
            file.write(response)
            print(f"Scraping in progress.. {round((i/48) * 100, 1)}% / 100%")
            

def write_to_pdf():
    img_list = [f"media/{i}.jpg" for i in range(1,49)]

    with open("result.pdf", "wb") as file:
        file.write(img2pdf.convert(img_list))

    print("PDF successfully created")

def main():
    get_data()
    write_to_pdf()


if __name__ == "__main__":
    main()