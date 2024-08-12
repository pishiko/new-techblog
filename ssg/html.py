from client import Article
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import sys

env = Environment(loader=FileSystemLoader('./template',encoding='utf-8'))

def create_article(article:Article,dist_path:str,template_path='index.html'):
    tmpl = env.get_template(template_path)
    html = tmpl.render(article=article)
    
    path = f'{dist_path}/{article.url}'
    os.mkdir(path)
    with open(f'{path}/index.html',mode='w',encoding='utf-8') as f:
        f.write(html)
    return

def create_top(articles:list[Article],dist_path:str,template_path='top.html'):
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

    out_dir = '../docs' if not mock else '../.preview'

    articles = get_articles(mock=mock)
    if articles:
        shutil.rmtree(out_dir,ignore_errors=True)
        os.makedirs(out_dir+'/posts')
        shutil.copytree('../html/dist/assets',out_dir+'/assets')
        shutil.copytree('../html/static',out_dir,dirs_exist_ok=True)

        for article in articles:
            create_article(article,dist_path=out_dir+'/posts')

        create_top(articles,dist_path=out_dir)
