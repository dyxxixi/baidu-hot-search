import requests
from bs4 import BeautifulSoup
import xlwt


def request_baidu(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('百度热搜榜', cell_overwrite_ok=True)
sheet.write(0, 0, '序号')
sheet.write(0, 1, '热搜标题')
sheet.write(0, 2, '内容')
sheet.write(0, 3, '热搜指数')

n = 1


def save_to_excel(soup):
    list = soup.find_all(class_='category-wrap_iQLoo horizontal_1eKyQ')
    for item in list:
        item_title = item.find(class_='c-single-text-ellipsis').text
        item_content = item.find(class_='hot-desc_1m_jR').text
        item_index = item.find(class_='hot-index_1Bl1a').text

        global n

        sheet.write(n, 0, n)
        sheet.write(n, 1, item_title)
        sheet.write(n, 2, item_content)
        sheet.write(n, 3, item_index)

        n = n + 1


def main():
    url = "https://top.baidu.com/board?tab=realtime"
    html = request_baidu(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


main()
book.save(u'百度热搜榜.xls')
