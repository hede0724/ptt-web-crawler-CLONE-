# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os

class TestCrawlerByPathTesting(unittest.TestCase):
    #   Path Testing
    
    #   21 -> 64
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
    
    #   21 -> 22 -> 23 -> 29 -> 63
    #   測試功能 : 爬取某個板內的文章，以 start 跟 end index 來決定爬取的文章範圍
    #   end index = -1 (= 整個版的 last article index)
    def test_path02(self):
        crawler(['-b', 'CoLoR_BAND', '-i', '0', '-1'])
        filename = 'CoLoR_BAND-0-9.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            self.assertEqual(len(jsondata['articles']),180)
        os.remove(filename)
        
    
    # #   21 -> 22 -> 26 -> 29 -> 63
    # def test_Path03(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 63
    # def test_Path04(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 63
    # def test_Path05(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 63
    # def test_Path06(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 63
    # def test_Path07(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 62 -> 63
    # def test_Path08(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 62 -> 63
    # def test_Path09(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 62 -> 63
    # def test_Path10(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 62 -> 63
    # def test_Path11(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 56 -> 49 -> 62 -> 63
    # def test_Path12(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 56 -> 49 -> 62 -> 63
    # def test_Path13(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 58-> 49 -> 62 -> 63
    # def test_Path14(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 58-> 49 -> 62 -> 63
    # def test_Path15(self):
        
    
    # #   21 -> 22 -> 23 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 49 -> 62 -> 63
    # def test_Path16(self):
        
    
    # #   21 -> 22 -> 26 -> 29 -> 36 -> 37 -> 47 -> 49 -> 50 -> 55 -> 49 -> 62 -> 63
    # def test_Path17(self):
        
    
if __name__ == '__main__':
    unittest.main()