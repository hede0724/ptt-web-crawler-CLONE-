# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os

class TestCrawlerByEquivalenceValeTest(unittest.TestCase):
    # Strong Robust Equivalence Testing
    # 測試函式 : python crawler.py -b 看板名稱 -a 文章ID
    # 功能 : 取得特定看板中，特定文章ID的相關內容
    
    # 測試情境 : 看板中確實包含該 ID的文章
    # 測試文章 : marvel 版， [其他] 柯受良死因
    def test_ValidInput_TheArticleMatchesTheBoardName_1st(self):
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
        
    # 測試情境 : 看板中確實包含該 ID的文章
    # 測試文章 :  Baseball 版， [炸裂] 蔣智賢炸裂
    def test_ValidInput_TheArticleMatchesTheBoardName_2nd(self):
        crawler(['-b', 'Baseball', '-a','M.1491912774.A.B3E'])
        filename = 'Baseball-M.1491912774.A.B3E.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            # 以文章的 (作者、ip、發文時間) 為 unique 的 data，驗證 crawler 得到的文章的正確性
            self.assertEqual(jsondata['author'], 'gtocat (糧草徵收人)')
            self.assertEqual(jsondata['ip'], '49.218.4.50')
            self.assertEqual(jsondata['date'], 'Tue Apr 11 20:12:51 2017')
            
            # 再次驗證 input 與 crawler 得到的相同
            self.assertEqual(jsondata['board'], 'Baseball')
            self.assertEqual(jsondata['article_id'], 'M.1491912774.A.B3E')
        os.remove(filename)
    
    # 測試情境 : 看板中確實包含該 ID的文章
    # 測試文章 :  NCTU_TALK 版， [討論] 交大人不可不交大事(幾近完整版)
    def test_ValidInput_TheArticleMatchesTheBoardName_3rd(self):
        crawler(['-b', 'NCTU_TALK', '-a','M.1451907241.A.D0D'])
        filename = 'NCTU_TALK-M.1451907241.A.D0D.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            # 以文章的 (作者、ip、發文時間) 為 unique 的 data，驗證 crawler 得到的文章的正確性
            self.assertEqual(jsondata['author'], 'sorryandbye (隨ｇ致富)')
            self.assertEqual(jsondata['ip'], '140.113.123.47')
            self.assertEqual(jsondata['date'], 'Mon Jan  4 19:33:37 2016')
            
            # 再次驗證 input 與 crawler 得到的相同
            self.assertEqual(jsondata['board'], 'NCTU_TALK')
            self.assertEqual(jsondata['article_id'], 'M.1451907241.A.D0D')
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  marvel 版， [炸裂] 蔣智賢炸裂 (Baseball版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_1st(self):
        crawler(['-b', 'marvel', '-a','M.1491912774.A.B3E'])
        filename = 'marvel-M.1491912774.A.B3E.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  NCTU_TALK 版， [炸裂] 蔣智賢炸裂 (Baseball版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_2nd(self):
        crawler(['-b', 'NCTU_TALK', '-a','M.1491912774.A.B3E'])
        filename = 'NCTU_TALK-M.1491912774.A.B3E.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  Baseball 版， [討論] 交大人不可不交大事(幾近完整版) (NCTU_TALK版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_3rd(self):
        crawler(['-b', 'Baseball', '-a','M.1451907241.A.D0D'])
        filename = 'Baseball-M.1451907241.A.D0D.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  marvel 版， [討論] 交大人不可不交大事(幾近完整版) (NCTU_TALK版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_4th(self):
        crawler(['-b', 'marvel', '-a','M.1451907241.A.D0D'])
        filename = 'marvel-M.1451907241.A.D0D.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  NCTU_TALK 版， [其他] 柯受良死因 (marvel 版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_5th(self):
        crawler(['-b', 'NCTU_TALK', '-a','M.1491738343.A.276'])
        filename = 'NCTU_TALK-M.1491738343.A.276.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板中沒有包含該 ID的文章
    # 測試文章 :  Baseball 版， [其他] 柯受良死因 (marvel 版中的文章)
    def test_ValidInput_TheArticleDoesNotMatchTheBoardName_6th(self):
        crawler(['-b', 'Baseball', '-a','M.1491738343.A.276'])
        filename = 'Baseball-M.1491738343.A.276.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            # json 檔案內剩下一個 key : error
            jsondata = json.load(f)
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
        
if __name__ == '__main__':
    unittest.main()