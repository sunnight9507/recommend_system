# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re


def is_possible_scraping(url: str) -> bool:
    """[summary]

    Args:
        url (str): [description]

    Returns:
        bool: [description]
    """

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        p = re.compile('alert\("([가-힣 .]+)"\);')
        result = p.search(str(soup))

        if result.group(1) == "영화 코드값 오류입니다.":  # 해당 url이 없는 경우
            return False
        return True
    else:
        return False


def scraping(url: str, code_list: list) -> dict:
    """[summary]

    Args:
        url (str): [description]
        code_list (list): [description]
    """

    for code in code_list:
        temp_url = url + code
        data = {}
        if is_possible_scraping(temp_url):
            print(temp_url)
            html = requests.get(temp_url).text
            soup = BeautifulSoup(html, "html.parser")

            # 영화 code
            data["code"] = int(code)
            # 영화 title
            data["movie_title"] = soup.select_one("h3.h_movie > a:nth-of-type(1)").text
            # TODO: try except가 좋은지?
            # 관람객 평점
            try:
                rating_text = soup.select_one(
                    "a.ntz_score > div.star_score > span.st_off > span.st_on"
                ).text
                data["audience_rating"] = float(re.findall("[\d.]+", rating_text)[0])
            except:
                print("해당 영화에 대한 정보가 없습니다.")
                continue
            # 기자 평론가 평점
            try:
                data["journalist_rating"] = float(
                    soup.select_one("a.spc > div.star_score").text.strip()
                )
            except:
                pass
            # 네티즌 평점
            try:
                data["netizen_rating"] = float(
                    soup.select_one("#pointNetizenPersentBasic").text
                )
            except:
                pass
            # 개요: 장르
            try:
                genre = soup.select_one(
                    "dl.info_spec > dd > p > span:nth-of-type(1)"
                ).text
                data["genre"] = set(map(lambda x: x.strip(), genre.split(",")))
            except:
                pass
            # 개요: 제작국가
            try:
                country_of_making = soup.select_one(
                    "dl.info_spec > dd > p > span:nth-of-type(2)"
                ).text
                data["country_of_making"] = set(
                    map(lambda x: x.strip(), country_of_making.split(","))
                )
            except:
                pass
            # 개요: 상영 시간
            try:
                data["running_time"] = soup.select_one(
                    "dl.info_spec > dd > p > span:nth-of-type(3)"
                ).text.strip()
            except:
                pass
            # 개요: 개봉 날짜
            try:
                release_date = soup.select_one(
                    "dl.info_spec > dd > p > span:nth-of-type(4)"
                ).text.split()
                data["release_date"] = "".join(release_date[-3:])
            except:
                pass
            # 감독
            try:
                data["director"] = soup.select_one(
                    "dl.info_spec > dd:nth-of-type(2) > p > a"
                ).text
            except:
                pass
            # 등급
            try:
                movie_grade = soup.select_one(
                    "dl.info_spec > dd:nth-of-type(4) > p"
                ).text.split()
                movie_grade = set(
                    movie_grade[index + 1].strip()
                    if value.strip() in {"[국내]", "[해외]"}
                    else ""
                    for index, value in enumerate(movie_grade)
                )
                movie_grade.discard("")
                data["movie_grade"] = movie_grade
            except:
                pass
            print(data)

        else:
            print("해당 url은 scraping 할 수 없습니다.")


def main():
    # TODO: scraping https://movie.naver.com/movie/bi/mi/basic.nhn?code=187310
    url = "https://movie.naver.com/movie/bi/mi/basic.nhn?code="
    code_list = ["31796", "187310", "1", "111111", "123455", "196051"]
    # code_list = ["31796", "187310"]
    scraping(url, code_list)


if __name__ == "__main__":
    main()
