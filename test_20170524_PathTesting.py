# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
import sys
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os
from io import StringIO

class TestCrawlerByPathTesting(unittest.TestCase):
    #   Path Testing      
    
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
    
    #   Path 03 : 21 -> 22 -> 26 -> 29 -> 63
    #   26 : 第二個 input value (end index) != -1
    #   36 failed : 不合法的輸入格式
    def test_Path03(self):
        crawler(['-b', 'CoLoR_BAND', '-i', '-1', '0'])
        filename = 'CoLoR_BAND--1-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            #self.assertEqual(len(data['articles']),11)
            self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
    
    #   Path 04 : 21 -> 22 -> 23 -> 29 -> 36 -> 63
    #   Path 06 : 21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 63
    #   Path 08 : 21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 62 -> 63 
    #   Path 10 : 21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 62 -> 63
    #   Path 12 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 62 -> 63
    #   Path 14 : 21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 58-> 49 -> 62 -> 63
    #   Path 16 : 21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 49 -> 62 -> 63
    
    #   23 : 第二個 input value (end index) == -1
    #   36 : valid input
    def test_Path04(self):
        crawler(['-b', 'Y2J', '-i', '0', '-1'])
        filename = 'Y2J-0-10.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),210)
        os.remove(filename)
    
    #   Path 05 : 21 -> 22 -> 26 -> 29 -> 36 -> 63
    #   Path 07 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 63
    #   Path 09 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 62 -> 63
    #   Path 11 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 62 -> 63
    #   Path 13 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 56 -> 49 -> 62 -> 63
    #   Path 15 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 58-> 49 -> 62 -> 63
    #   Path 17 : 21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 49 -> 62 -> 63
    
    #   26 : 第二個 input value (end index) != -1
    #   36 : valid input
    def test_Path05(self):
        crawler(['-b', 'Y2J', '-i', '0', '10'])
        filename = 'Y2J-0-10.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),210)
        os.remove(filename)
            
if __name__ == '__main__':
    unittest.main()