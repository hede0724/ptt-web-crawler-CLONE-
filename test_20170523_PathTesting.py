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
    
    #   Path01 : 21 -> 64
    #   測試功能 :  尋找某個版內是否存在某個 article_id 是否存在，
    #   若存在則回傳 文章的相關資訊，若否則會傳 'error'
    def test_Path01(self):
        crawler(['-b', 'marvel', '-a','M.1491738343.A.276'])
        filename = 'marvel-M.1491738343.A.276.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            # 以文章的 (作者、ip、發文時間) 為 unique 的 data，驗證 crawler 得到的文章的正確性
            self.assertEqual(jsondata['author'], 'ajemtw (Dream Out Loud)')
            self.assertEqual(jsondata['ip'], '118.169.160.99')
            self.assertEqual(jsondata['date'], 'Sun Apr  9 19:45:41 2017')
            
            # 再次驗證 input 與 crawler 得到的相同
            self.assertEqual(jsondata['board'], 'marvel')
            self.assertEqual(jsondata['article_id'], 'M.1491738343.A.276')
        os.remove(filename)
    
    #   Path02 : 21 -> 22 -> 23 -> 29 -> 63
    #   測試功能 : 爬取某個板內的文章，以 start 跟 end index 來決定爬取的文章範圍
    #   23 : end index = -1 (= 整個版的 last article index)
    #   36 failed : 不合法的輸入
    def test_path02(self):
        crawler(['-b', 'CoLoR_BAND', '-i', '-2', '-1'])
        filename = 'CoLoR_BAND--2--10.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            #self.assertEqual(len(data['articles']),11)
            self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
        
if __name__ == '__main__':
    unittest.main()