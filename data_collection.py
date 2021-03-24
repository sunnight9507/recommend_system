# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re


def scraping(url):
    """
    해당 url scraping

    Args:
        url ([type]): [description]
    """
    
    response = requests.get(url)
    if response.status_code == 200:
        data = {}
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 영화 title
        data["movie_title"] = soup.select_one("h3.h_movie > a:nth-of-type(1)").text
        # 관람객 평점
        rating_text = soup.select_one("a.ntz_score > div.star_score > span.st_off > span.st_on").text
        data["audience_rating"] = float(re.findall("[\d.]+", rating_text)[0])

        # print(test)
        print(data)
    else:
        print(response.status_code)


def main():
    # TODO: scraping https://movie.naver.com/movie/bi/mi/basic.nhn?code=187310
    url = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=187310"
    scraping()


if __name__ == "__main__":
    main()
