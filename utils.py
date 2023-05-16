"""
this file is all kind of small tools
author: jarvis
time: 2021-5-1
Attention: we will use "tmp" dir to keep ts files
"""
import logging
import os
import shutil
import urllib.request

import m3u8
import win32event
import win32process
from win32com.client import Dispatch

logger = logging.getLogger(__name__)


def download_by_tool(url, filename):
    exe_path = r"E:\\迅雷下载\\91pron_python-main\\m3u8DL-CLI\\N_m3u8DL-CLI_v2.9.1.exe"
    your_command = r' "{}" --workDir "E:\\tmp" --saveName "{}" --enableDelAfterDone'.format(url, filename)
    test_com = r" https://la.killcovid2021.com/m3u8/591161/591161.m3u8 --workDir E:\\tmp --saveName success --enableDelAfterDone"
    try:
        handle = win32process.CreateProcess(exe_path,
                                            your_command,
                                            None,
                                            None,
                                            0,
                                            win32process.CREATE_NO_WINDOW,
                                            None,
                                            r"E:\\迅雷下载\\91pron_python-main\\m3u8DL-CLI",
                                            win32process.STARTUPINFO())
        running = True
    except Exception as Argument:
        logging.info("Create Error!", Argument)
        handle = None
        running = False

    while running:
        rc = win32event.WaitForSingleObject(handle[0], 1000)
        if rc == win32event.WAIT_OBJECT_0:
            running = False
    # end while
    print("finish!")


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
    download_by_tool("https://la.killcovid2021.com/m3u8/591161/591161.m3u8", "aaa")
