from client import Article
from jinja2 import Environment, FileSystemLoader
import os
import shutil

env = Environment(loader=FileSystemLoader('./template',encoding='utf-8'))

def create_article(article:Article,template_path='index.html',dist_path='../public/posts'):
    tmpl = env.get_template(template_path)
    html = tmpl.render(article=article)
    
    path = f'{dist_path}/{article.url}'
    os.mkdir(path)
    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:
        f.write(html)
    return

def create_top(articles:list[Article],template_path='top.html',dist_path='../public'):
    tmpl = env.get_template(template_path)
    html = tmpl.render(articles=articles)
    
    path = f'{dist_path}/'
    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:
        f.write(html)
    return


if __name__ == '__main__':
    from client import get_articles
    articles = get_articles()
    if articles:
        shutil.rmtree('../public')
        os.makedirs('../public/posts')
        shutil.copytree('../html/dist/assets','../public/assets')

        for article in articles:
            create_article(article)

        create_top(articles)
