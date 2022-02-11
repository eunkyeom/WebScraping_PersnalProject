# 네이버 오늘의 날씨 정보 스크래핑

from types import NoneType
import requests
from bs4 import BeautifulSoup
import re


def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    
    # 오늘 날씨 : ex) 어제보다 1° 높아요  맑음
    summary = soup.find("p", attrs={"class":"summary"}).get_text()
    print(summary)
    print("")

    # 현재 온도 (최저 온도 / 최고 온도)
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text().replace(" 현재 온도", "") # 4°
    print(f"현재 온도 : {curr_temp}")

    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text().replace("최저기온", "") # -4°
    print(f"최저 온도 : {min_temp}")

    max_temp = soup.find("span", attrs={"class":"highest"}).get_text().replace("최고기온", "") # 6°
    print(f"최고 온도 : {max_temp}")

    # 오전 강수확률 OO%, 오후 강수확률 OO%
    rainfall = soup.find_all("span", attrs={"class":"weather_left"})
    for idx, rainfall_idx in enumerate(rainfall):
        if idx == 0:
            rainfall_morning = rainfall_idx
            print("")
            print("강수 확률 :", rainfall_morning.get_text())
        elif idx == 1:
            rainfall_afternoon = rainfall_idx
            print("강수 확률 :", rainfall_afternoon.get_text())
    
    # 미세먼지
    dusts = soup.find("li", attrs={"class":"item_today level1"})
    # print(dusts[0].find("li", attrs={"class":"item_today level1"}))
    dusts = dusts.get_text()[2:]
    print("")
    print(dusts)


def scrape_headline_news():
    print()
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"native_scroll_list cjs_headline_list"}).find_all("li")#, limit = 2
    for idx, news in enumerate(news_list):
        title = news.find("div").get_text()
        link = news.find("a")["href"]
        print("{}. {}".format(idx + 1, title))
        print("  (링크 : {}".format(link))


def scrape_it_news():
    print()
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":["type06_headline", "type06"]}).find_all("li")
    # print(news_list)
    for idx, news in enumerate(news_list):
        try:
            title = news.find("img")["alt"]
            print("{}. {}".format(idx + 1, title))
        except:
            #title = "No title"
            print("기사 없음")
        # thumbnail_tag = news.select_one('div > a > img') 
        # if thumbnail_tag is None: 
        #     thumbnail = "" 
        # else: 
        #     thumbnail = thumbnail_tag["src"]


def scrape_english():
    print()
    print("[오늘의 영어회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})

    print("영어지문")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때 4~7까지 잘라서 가져옴 (반만 가져옴), [8/2를 한 인덱스부터]:끝까지
        print(sentence.get_text().strip())
    
    print()
    print("한글 지문")
    for sentence in sentences[:len(sentences)//2]: # 처음부터 :[8/2를 한 인덱스까지]
        print(sentence.get_text().strip())


if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨정보 가져오기, 직접 실행할 때만 동작하도록 함수 정의, 다른 파일에 의해서 호출될 때는 실행이 되지 않도록
    #scrape_headline_news()  # 헤드라인 뉴스 정보 가져오기 (현재 헤드라인 항목이 없어짐)
    scrape_it_news() # IT 뉴스 가져오기
    scrape_english() # 해커스 오늘의 회화 가져오기

