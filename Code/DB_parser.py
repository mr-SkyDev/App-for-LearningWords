import csv
import sqlite3
import requests
from bs4 import BeautifulSoup
from time import sleep


URL = "https://en-rus-sleng-dict.slovaronline.com/"


def get_html(url):
    try:
        r = requests.get(url)
        if not r.ok:
            print(r.status_code)
            quit()
        return r.text
    except:
        print("error")


def get_data(html):
    soup = BeautifulSoup(html, "lxml")

    words_div = soup.find_all("div", class_="article-link")
    words_link = [div.findChildren("a") for div in words_div]
    # words_text = [word[0].text for word in words_link]

    # data = list()
    for a in words_link:
        link = a[0].get("href")
        link_soup = BeautifulSoup(get_html(URL + link), "lxml")
        value = link_soup.find("div", class_="blockquote").text.strip()

        # data.append({
        #     'word': a[0].text.strip(),
        #     'value': value
        # })
        data = {
            'word': a[0].text.strip(),
            'value': value
        }
        write_csv(data, "en-rus-sleng.csv")
        sleep(0.2)
        print(link)


def write_csv(data, filename):
    with open(filename, "a", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["word", "value"],
            delimiter=";",
            quotechar='"',
            lineterminator="\n",
        )
        # writer.writeheader()
        # for line in data:
        writer.writerow(data)


def write_db(data):
    ...


def main():
    # Парсер английского сленга
    data = get_data(get_html(URL))
    # write_csv(data, "en-rus-sleng.csv")


if __name__ == "__main__":
    main()
