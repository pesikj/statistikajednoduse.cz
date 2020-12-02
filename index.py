from flask import Flask, render_template, request
from markdown2 import Markdown
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
import yaml
import io
from tails import Tail
app = Flask(__name__)

import images
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response


def get_page_info(folder, page):
    info = open('content.yaml', 'r', encoding="utf-8")
    info = yaml.load(info, Loader=yaml.BaseLoader)
    return info[folder][page]

def process_lesson_html(html):
    soup = BeautifulSoup(html)
    links = []
    for item in soup.findAll('img'):
        item['class'] = 'responsive-img'
    for item in soup.findAll('li'):
        item['style'] = 'list-style-type: initial; list-style-position: inside;'
    for heading in soup.findAll(re.compile('^h[1-6]$')):
        id = unidecode(heading.string.lower().replace(" ", "-"))
        heading["id"] = id
        if heading.name == "h2":
            links.append([id, heading.string])
    html = str(soup)
    return html, links

@app.route('/images/cr//')
@app.route('/images/cr/<distribution>/')
@app.route('/images/cr/<distribution>/<tail>/')
def get_image(distribution="norm", tail=0):
    fig = images.create_critical_region_plot(distribution, Tail.TWO_TAILED)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/lesson/<folder>/<page>', defaults={'number': 1})
@app.route('/lesson/<folder>/<page>/<number>')
def read_lesson(folder, page, number):
    markdowner = Markdown(extras=["tables"])
    data = open(f"content/{folder}/{page}/{number}.md", 'r', encoding="utf-8").read()
    lesson_content, links = process_lesson_html(markdowner.convert(data))
    info = get_page_info(folder, page)
    return render_template('lesson.html', lesson_content=lesson_content, title=info['title'], links=links)

@app.route('/')
def hello_world():
    return render_template('index.html')
