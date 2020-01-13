import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908 ',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

musics = soup.select('#body-content >div.newest-list > div >  table > tbody > tr')


# newest-list > #music-list-wrap >

# movies (tr들) 의 반복문을 돌리기
rank = 1
for music in musics:
    # movie 안에 a 가 있으면,
    a_tag = music.select_one('td.info > a.title.ellipsis')
    if a_tag is not None:
        name = a_tag.text
        sing = music.select_one('td.info > a.artist.ellipsis').text
        print(rank, name.strip() ,sing.strip())


        doc = {
            'rank': rank,
            'name': name,
            'sing': sing
        }
        db.songs.insert_one(doc)
        rank += 1
