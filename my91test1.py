"""
@author caijiawei
@time 2020-09-10
"""
import csv
import logging
import random

import requests
from lxml import etree

import web_parser

logging.basicConfig(level=logging.INFO)


def show_videos_info(url, title, film_view, film_collection, score, author):
    print(url)
    print(title)
    print('作者：', author)
    print(film_view, film_collection, end=' ' * 6)
    print(score)
    print('-' * 40)


def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)


def write_info_to_csv(rows):
    headers = ['file_name', 'url']

    with open('info.csv', 'w', newline='', encoding="utf-8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


def main(page_num=3, threshold_score=3, flag=1, catalogue_url=None):
    """"""
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    global res
    res = []
    video_cnt = 0
    while flag <= page_num:
        print('当前页面数为：', flag)
        page_url = catalogue_url + str(flag)  # 本月最热视频展示页
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                   'X-Forwarded-For': random_ip(), 'referer': page_url,
                   'Content-Type': 'multipart/form-data; session_language=cn_CN',
                   }
        get_page = requests.get(url=page_url, headers=headers, verify=False)
        get_page.encoding = 'utf-8'  # 注意网站的中文编码格式问题
        html = etree.HTML(get_page.text)
        viewkey = html.xpath('//div[@class="col-xs-12 col-sm-4 col-md-3 col-lg-3"]')
        for key in viewkey:
            title = key.xpath('./div/a/span[@class="video-title title-truncate m-t-5"]/text()')[0].strip()  #
            author = key.xpath('./div/text()[6]')[0].strip()
            film_view = key.xpath('./div/text()[8]')[0].strip()
            film_collection = key.xpath('./div/text()[9]')[0].strip()
            score = round(int(film_collection) / int(film_view) * 1000, 2)
            url = key.xpath("./div/a/@href")[0]  # 获得具体视频内容页面链接
            if score >= threshold_score:  # 比较阈值
                video_cnt += 1
                show_videos_info(url, title, film_view, film_collection, score, author)
                res.append([title + "({})".format(score), url])
                # enter_second_page(url, headers)
                web_parser.parse_two_class_web(url, headers)
                print("video_cnt:", video_cnt)
        flag += 1
    write_info_to_csv(res)


if __name__ == '__main__':
    page_num = 5  # 设置爬取网页数upper bound，total 5
    flag = 1  # from which page begin
    threshold_score = 5  # 设置下载视频阈值
    IP_address = 'https://0118.workarea7.live/'
    # IP_address = 'http://www.91porn.com'
    this_month_most_hot_page = IP_address + '/v.php?category=top&viewtype=basic&page='  # 本月最热视频展示页
    last_month_most_hot_page = IP_address + '/v.php?category=top&m=-1&viewtype=basic&page='  # 上月最热视频展示页
    video_list = IP_address + '/v.php?next=watch&page='
    this_month_discuss = IP_address + '/v.php?category=md&viewtype=basic&page='
    this_month_collection_most = IP_address + '/v.php?category=tf&viewtype=basic&page='
    all_website_collection_most = IP_address + '/v.php?category=mf&viewtype=basic&page='

    main(page_num=page_num, threshold_score=threshold_score, flag=flag, catalogue_url=last_month_most_hot_page)
