# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os

class TestCrawlerByBoundaryValueTest(unittest.TestCase):
    def  test_parse(self) :
        self.link = 'https://www.ptt.cc/bbs/HatePolitics/M.1417187870.A.722.html';
        self.article_id = 'M.1417187870.A.722'
        self.board = 'HatePolitics'
        self.author = 'twflash (.....)'
        
        jsondata = json.loads(crawler.parse(self.link, self.article_id, self.board) )
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)
        self.assertEqual(jsondata['author'], self.author)

    def test_crawler_StartIndexMinimumValueMinus(self):
        crawler(['-b', 'NBA', '-i', '-1', '0'])
        filename = 'NBA--1-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),11)
        os.remove(filename)
        
    def test_crawler_StartIndexMinimumValue(self):
        crawler(['-b', 'NBA', '-i', '0', '0'])
        filename = 'NBA-0-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),11)
        os.remove(filename)
        
    def test_crawler_StartIndexMinimumValuePlus(self):
        crawler(['-b', 'NBA', '-i', '1', '0'])
        filename = 'NBA-1-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),0)
        os.remove(filename)
        
if __name__ == '__main__':
    unittest.main()