from flask import Flask, render_template
from markdown2 import Markdown
from bs4 import BeautifulSoup
from unidecode import unidecode
import yaml
app = Flask(__name__)


def get_page_info(folder, page):
    info = open('content.yaml', 'r')
    info = yaml.load(info, Loader=yaml.BaseLoader)
    return info[folder][page]

def process_lesson_html(html):
    soup = BeautifulSoup(html)
    links = []
    for link in soup.findAll('img'):
        link['class'] = 'responsive-img'
    for heading in soup.findAll('h2'):
        id = unidecode(heading.string.lower().replace(" ", "-"))
        heading["id"] = id
        links.append([id, heading.string])
    html = str(soup)
    return html, links

@app.route('/lesson/<folder>/<page>', defaults={'number': 1})
@app.route('/lesson/<folder>/<page>/<number>')
def read_lesson(folder, page, number):
    markdowner = Markdown(extras=["tables"])
    data = open(f"content/{folder}/{page}/{number}.md", 'r').read()
    lesson_content, links = process_lesson_html(markdowner.convert(data))
    info = get_page_info(folder, page)
    return render_template('lesson.html', lesson_content=lesson_content, title=info['title'], links=links)

@app.route('/')
def hello_world():
    return render_template('index.html')
