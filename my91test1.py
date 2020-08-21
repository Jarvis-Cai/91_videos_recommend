# author：caijiawei
# time:2019.7.5
import random
from lxml import etree
import requests, js2py, re
from win32com.client import Dispatch
import csv


def use_thunder_download(url, filename):
    """
    use thunder downloading
    :param url:
    :param filename:
    :return: none
    """
    print('use thunder downloading...')
    thunder = Dispatch('ThunderAgent.Agent64.1')
    thunder.AddTask(url, filename)
    thunder.CommitTasks()


def use_request_to_download(url, filename):
    """
    this style of downloading maybe be faster
    :param url:
    :param filename:
    :return: none
    """
    print('use python downloading...')
    directory = 'G:\\电影\\'
    filename = directory + filename
    for i in range(10):
        try:
            req = requests.get(url=url)
            with open(filename, 'wb') as f:
                f.write(req.content)
        except:
            print('please pay attention, I am trying for the %d times'%i)
            continue
        break


def enter_second_page(url, headers, js):
    global res
    s = requests.session()
    s.keep_alive = False
    get_page = s.get(url=url, headers=headers, verify=False).content.decode('utf-8')
    # print(get_page)  # this is just for test
    url = parse_url_in_second_page(get_page, js)  # 这个用了js加密处理

    key = etree.HTML(get_page)
    title = key.xpath('//*[@id="videodetails"]/h4/text()')[0].strip()
    # url = key.xpath('//*[@id="player_one_html5_api"]/source/@src')[0]
    # author = key.xpath('./text()[9]')[0].lstrip()
    film_view = key.xpath('//*[@id="useraction"]/div[1]/span[2]/span/text()')[0].strip()
    film_collection = key.xpath('//*[@id="useraction"]/div[1]/span[4]/span/text()')[0].strip()
    score = round(int(film_collection) / int(film_view) * 1000, 2)
    title = title + '(' + str(score) + ')' + '.mp4'
    print(url)
    res.append((title, url[0]))
    # use_thunder_download(url[0], title)  # maybe we should choose which one to download
    # use_request_to_download(url[0], title)


def show_videos_info(url, title, film_view, film_collection, score, author):
    print(url)
    print(title)
    print('作者：', author)
    print(film_view, film_collection, end=' ' * 6)
    print(score)
    print('-'*40)


def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)


def write_info_to_csv(rows):
    headers = ['file_name', 'url']

    with open('info.csv', 'w', newline='', encoding="utf-8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


def parse_url_in_second_page(get_page, js):
    """解决js加密问题"""
    ifm = re.findall('strencode\((.*?)\)', get_page)
    print(ifm)
    ifm[0] = ifm[0].replace('"', '')
    ifm = js.strencode(ifm[0].split(',')[0], ifm[0].split(',')[1], ifm[0].split(',')[2])  # this is object url
    # print(ifm, '嘻嘻')
    video_url = re.findall(r"<source src='(.*?)' type=\'video/mp4\'>", ifm)
    return video_url  # 这是一个元素的list


def main(page_num=3, threshold_score=3, flag=1, catalogue_url=None):
    """"""
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    jsdata = requests.get(IP_address+"/js/md5.js").text
    js = js2py.EvalJs()
    js.execute(jsdata)
    global res
    res = []
    while flag <= page_num:
        print('当前页面数为：', flag)
        page_url = catalogue_url+str(flag)  # 本月最热视频展示页
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                   'X-Forwarded-For': random_ip(), 'referer': page_url,
                   'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        get_page = requests.get(url=page_url, headers=headers, verify=False)
        get_page.encoding = 'utf-8'  # 注意网站的中文编码格式问题
        html = etree.HTML(get_page.text)
        viewkey = html.xpath('//div[@class="col-xs-12 col-sm-4 col-md-3 col-lg-3"]')
        for key in viewkey:
            title = key.xpath('./div/a/span[@class="video-title title-truncate m-t-5"]/text()')[0].strip()  #
            author = key.xpath('./div/text()[7]')[0].strip()
            film_view = key.xpath('./div/text()[9]')[0].strip()
            film_collection = key.xpath('./div/text()[10]')[0].strip()
            score = round(int(film_collection) / int(film_view) * 1000, 2)
            url = key.xpath("./div/a/@href")[0]  # 获得具体视频内容页面链接
            if score >= threshold_score:  # 比较阈值
                show_videos_info(url, title, film_view, film_collection, score, author)
                enter_second_page(url, headers, js)
        flag += 1
    write_info_to_csv(res)


if __name__ == '__main__':
    page_num = 5  # 设置爬取网页数upper bound，total 5
    flag = 1  # from which page begin
    threshold_score = 4  # 设置下载视频阈值
    IP_address = 'https://627.workarea8.live'
    # IP_address = 'http://www.91porn.com'
    this_month_most_hot_page = IP_address + '/v.php?category=top&viewtype=basic&page='  # 本月最热视频展示页
    last_month_most_hot_page = IP_address + '/v.php?category=top&m=-1&viewtype=basic&page='  # 上月最热视频展示页
    video_list = IP_address + '/v.php?next=watch&page='
    this_month_discuss = IP_address + '/v.php?category=md&viewtype=basic&page='
    this_month_collection_most = IP_address + '/v.php?category=tf&viewtype=basic&page='
    all_website_collection_most = IP_address + '/v.php?category=mf&viewtype=basic&page='

    main(page_num=page_num, threshold_score=threshold_score, flag=flag, catalogue_url=last_month_most_hot_page)
