from unittest import TestCase
import unittest
import logging

import sys
sys.path.append("../")
import utils

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):
    def test_downloader(self):
        utils.downloader('https://la.killcovid2021.com/m3u8/591161/591161.m3u8')

    def test_make_ts_2_mp4(self):
        utils.make_ts_2_mp4("test.mp4")


if __name__ == '__main__':
    unittest.main()
