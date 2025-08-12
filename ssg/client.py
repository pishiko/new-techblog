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

def _mock():
    return {
        "contents": [{
            "id": "9yew96t-9",
            "createdAt": "2023-04-18T15:19:22.081Z",
            "updatedAt": "2024-07-07T11:03:19.773Z",
            "publishedAt": "2023-04-18T15:19:22.081Z",
            "revisedAt": "2024-07-07T11:03:19.773Z",
            "title": "blog preview test",
            "content": "<h1 id=\"h3a671e7a37\">h1 hello world こんにちは 世界</h1><h2 id=\"hacd73a9c92\"><br>h2 goodbye world さようなら 世界</h2><h3 id=\"hf806f4c6b5\"><br>h3 good morning world おはよう 世界</h3>リポジトリ：<br><a href=\"https://github.com/pishiko/tenmusu/\" target=\"_blank\" rel=\"noopener noreferrer\">https://github.com/pishiko/tenmusu</a> <br><p><br>あの<code>イーハトーヴォ</code>のすきとおった風、夏でも底に冷たさをもつ青いそら、<s>うつくしい</s>森で飾られた<em>モリーオ</em>市、<strong>郊外</strong>のぎらぎらひかる草の波。<br><br><span style=\"color:#262626\">Lorem ipsum dolor sit amet, </span><code>consectetuer adipiscing elit</code><span style=\"color:#262626\">. </span><s style=\"color:#262626\">Maecenas porttitor congue massa</s><span style=\"color:#262626\">. </span><em style=\"color:#262626\">Fusce posuere</em><span style=\"color:#262626\">, magna sed </span><strong style=\"color:#262626\">pulvinar ultricies</strong><span style=\"color:#262626\">, purus lectus malesuada libero, sit amet commodo magna eros quis urna.</span><br></p><pre><code>import os\nimport shutil\n\n\nenv = Environment(loader=FileSystemLoader('./template',encoding='utf-8'))\n\n\ndef create_article(article:Article,template_path='index.html',dist_path='../docs/posts'):\n    tmpl = env.get_template(template_path)\n    html = tmpl.render(article=article)\n    \n    path = f'{dist_path}/{article.url}'\n    os.mkdir(path)\n    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:\n        f.write(html)\n    return</code></pre><p><br></p><blockquote>あのイーハトーヴォのすきとおった風、夏でも底に冷たさをもつ青いそら、うつくしい森で飾られたモリーオ市、郊外のぎらぎらひかる草の波。</blockquote><p><br></p><ul><li>hoge</li><li>fuga<ul><li>nyan</li><li>waiwai<ul><li>oioi</li></ul></li></ul></li><li>gyaogyao</li><li>wanwan</li></ul><p><br><a href=\"unsafe:p4ko.com\">p4ko.com</a><br><br><img src=\"https://images.microcms-assets.io/assets/a2f12ba91908497eab61a90567442944/613bcc363e02428ba38294d08b3095b3/266706774-a9c8dcca-e122-4425-94c2-d6eb0d6b30f7.png\" alt=\"\"><br></p><ol><li>tang<ol><li>keke</li></ol></li><li>sumire<ol><li>heanna</li></ol></li></ol><p><br></p><blockquote class=\"twitter-tweet\"><p lang=\"ja\" dir=\"ltr\">ザルを使わずにそうめんを冷やす技術</p>&mdash; pishiko (@pishitaro_) <a href=\"https://twitter.com/pishitaro_/status/1820697908796117313?ref_src=twsrc%5Etfw\">August 6, 2024</a></blockquote><script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script><p><br></p><iframe class=\"embedly-embed\" src=\"https://cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fwww.youtube.com%2Fembed%2FA1bleJVhZeY%3Ffeature%3Doembed&display_name=YouTube&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DA1bleJVhZeY&image=https%3A%2F%2Fi.ytimg.com%2Fvi%2FA1bleJVhZeY%2Fhqdefault.jpg&key=94335756f04b424b8ce3ce71cbe3de0a&type=text%2Fhtml&schema=youtube\" width=\"560\" height=\"315\" scrolling=\"no\" title=\"YouTube embed\" frameborder=\"0\" allow=\"autoplay; fullscreen; encrypted-media; picture-in-picture;\" allowfullscreen=\"true\"></iframe><p><br></p>",
            "url": "preview_test"
        }],
        "totalCount": 1,
        "offset": 0,
        "limit": 10
        }

def get_articles(mock=False):
    offset = 0
    articles:list[Article] = []

    while True:
        if not mock:
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
        else:
            j = _mock()
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