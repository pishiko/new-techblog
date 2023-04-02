import requests
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URI = os.getenv('API_BASE_URI')
MICROCMS_TOKEN = os.getenv('MICROCMS_TOKEN')

if not MICROCMS_TOKEN:
    MICROCMS_TOKEN = ""

@dataclass
class Article:
    url:str
    published_at:str
    title:str
    html:str

def get_articles():
    offset = 0
    articles:list[Article] = []

    while True:
        r = requests.get(f"{API_BASE_URI}blogs",
            params={
                'limit': 10,
                'offset': offset,
                'orders': '-publishedAt'
            },
            headers={
                "X-MICROCMS-API-KEY":MICROCMS_TOKEN
            })
        if r.status_code != 200:
            print(f"fetch failed {r.status_code}:{r.text}")
            return None
        j = r.json()
        for content in j["contents"]:
            published_at = datetime.fromisoformat(content["publishedAt"])
            articles.append(Article(
                url = content["url"],
                published_at = published_at.strftime('%Y-%m-%d'),
                title=content["title"],
                html = content["content"],
            ))
        offset += len(j['contents'])
        if j['totalCount'] <= len(articles):
            break
    return articles

if __name__ == "__main__":
    print(get_articles())