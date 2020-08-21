# author: caijiawei
# time: 2020.1.1
import requests, js2py
from lxml import etree
from my91test1 import random_ip, use_thunder_download, enter_second_page

url = [
'http://627.workarea8.live/view_video.php?viewkey=13474ce368150008dcb3&page=1&viewtype=basic&category=top',

]

IP_address = 'https://0112.workarea4.live'
jsdata = requests.get(IP_address+"/js/md5.js").text
js = js2py.EvalJs()
js.execute(jsdata)

for i in url:
	headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
			   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
			   'X-Forwarded-For': random_ip(), 'referer': i,
			   'Content-Type': 'multipart/form-data; session_language=cn_CN'
		}
	enter_second_page(i, headers, js)
