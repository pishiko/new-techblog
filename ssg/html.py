from client import Article
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import sys

env = Environment(loader=FileSystemLoader('./template',encoding='utf-8'))

def create_article(article:Article,template_path='index.html',dist_path='../docs/posts'):
    tmpl = env.get_template(template_path)
    html = tmpl.render(article=article)
    
    path = f'{dist_path}/{article.url}'
    os.mkdir(path)
    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:
        f.write(html)
    return

def create_top(articles:list[Article],template_path='top.html',dist_path='../docs'):
    tmpl = env.get_template(template_path)
    html = tmpl.render(articles=articles)
    
    path = f'{dist_path}/'
    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:
        f.write(html)
    return


if __name__ == '__main__':
    from client import get_articles

    args = sys.argv[1:]
    mock = '--mock' in args or '-m' in args# モック生成フラグ

    articles = get_articles(mock=mock)
    if articles:
        shutil.rmtree('../docs')
        os.makedirs('../docs/posts')
        shutil.copytree('../html/dist/assets','../docs/assets')
        shutil.copytree('../html/static','../docs',dirs_exist_ok=True)

        for article in articles:
            create_article(article)

        create_top(articles)
