from unittest import TestCase
import unittest
import sys
sys.path.append("..")
import utils


class Test(TestCase):
    def test_downloader(self):
        utils.downloader('https://cdn.91p07.com//m3u8/462096/462096.m3u8?st=6eSUS5im7OKlQO3BWV3-tA&e=1619859687')

    def test_make_ts_2_mp4(self):
        utils.make_ts_2_mp4("2.mp4")


if __name__ == '__main__':
    unittest.main()
