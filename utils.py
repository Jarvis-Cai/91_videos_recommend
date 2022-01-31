"""
this file is all kind of small tools
author: jarvis
time: 2021-5-1
Attention: we will use "tmp" dir to keep ts files
"""
import m3u8
import urllib.request
import os
import logging
import shutil
from win32com.client import Dispatch
import win32api
import subprocess


logger = logging.getLogger(__name__)


def download_by_tool(url, filename):
    exe_path = r"E:\迅雷下载\91pron_python-main\N_m3u8DL-CLI_v2.9.7.exe"
    your_command = r'"{}" --workDir "E:\tmp" --saveName "{}" --enableDelAfterDone'.format(url, filename)
    last_shell = exe_path + " " + your_command
    aa = r"E:\迅雷下载\91pron_python-main\N_m3u8DL-CLI_v2.9.7.exe https://cdn.91p07.com//m3u8/442236/442236.m3u8?st=xZMvsTd-PuHmhqdLU1DwnQ&e=1619871695 --workDir E:\tmp --saveName aaabbb --enableDelAfterDone"
    bb = ["E:\迅雷下载\91pron_python-main\\N_m3u8DL-CLI_v2.9.7.exe", "https://cdn.91p07.com//m3u8/442236/442236.m3u8?st=xZMvsTd-PuHmhqdLU1DwnQ&e=1619871695","--workDir E:\\tmp","--saveName aaabbb","--enableDelAfterDone"]
    p = subprocess.call(bb)
    p.wait()

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


def downloader(url):
    """
    :param url: 'https://cdn.91p07.com//m3u8/462096/462096.m3u8?st=6eSUS5im7OKlQO3BWV3-tA&e=1619859687'
    :return: ts files in tmp dir
    """
    # clear tmp dir first
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
        os.mkdir("tmp")
    else:
        os.mkdir("tmp")
    download_url = os.path.dirname(url)
    logger.debug(download_url)
    playlist = m3u8.load(url)  # this could also be an absolute filename
    print(playlist.segments.uri)
    uris = playlist.segments.uri
    for i in uris:
        a = download_url + '/' + i
        logger.debug(a)
        urllib.request.urlretrieve(a, "tmp/" + i)
        print("finish downoad {}".format(i))


def make_ts_2_mp4(file_name):
    """
    make_ts_2_mp4
    :param file_name: file name with postfix .mp4
    :return:
    """
    a_file = os.listdir("tmp")
    a_file.sort(key=lambda x: int(x.split('.')[0]))  # sort files by their index
    logger.debug(a_file)
    with open(file_name, 'ab') as f:
        for i in a_file:
            with open(os.path.join("tmp", i), 'rb') as g:
                a_ts = g.read()
            f.write(a_ts)


if __name__ == "__main__":
    download_by_tool("https://cdn.91p07.com//m3u8/442236/442236.m3u8?st=xZMvsTd-PuHmhqdLU1DwnQ&e=1619871695", "aaa")
