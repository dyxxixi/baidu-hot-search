import requests
from bs4 import BeautifulSoup
import json


def request_baidu(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def filter_data(soup):
    n = 1
    list = soup.find_all(class_='category-wrap_iQLoo horizontal_1eKyQ')
    dataArr = []

    for item in list:
        item_title = item.find(class_='c-single-text-ellipsis').text
        item_content = item.find(class_='hot-desc_1m_jR').text
        item_hotScore = item.find(class_='hot-index_1Bl1a').text
        dataArr.append({"id": n, "title": item_title,
                       "content": item_content, "hotScore": item_hotScore})
        n = n + 1
    return dataArr


def handler(environ, start_response):
    html = request_baidu("https://top.baidu.com/board?tab=realtime")
    soup = BeautifulSoup(html, 'lxml')
    data = filter_data(soup)
    respData = {
        "code": 200,
        "msg": "ok",
        "data": data
    }
    start_response('200 OK', [('Content-Type', 'text/html')])
    return json.dumps(respData)
