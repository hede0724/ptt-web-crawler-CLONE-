# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os

class TestCrawlerByDecisionBasedTableTesting(unittest.TestCase):
    # Decision-based Table Testing

    # Conditons                             Rule 1      Rule 2      Rule 3
    #   輸入看板名稱                   False         True         True
    #   看板中存在該ID文章        -             False         True
    # Action
    #                                              Invalid      Invalid    Output
    #                                                   URL           URL     JsonData
    
   # 測試函式 : python crawler.py -b 看板名稱 -a 文章ID
   # 功能 : 取得特定看板中，特定文章ID的相關內容
   
    # 測試情境 : 看板不存在 (Rule 1)
    # 測試文章 : _NBA 版 (虛構)， [花邊] 美國媒體對於籃網輪休感到不可思議 (NBA版中的文章)
   def test_Rule1_BoardDoesNotExist(self):
        crawler(['-b', '_NBA', '-a', 'M.1491980650.A.3ED'])
        filename = '_NBA-M.1491980650.A.3ED.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    
    # 測試情境 : 看板存在，但看板中並不存在該ID的文章 (Rule 2)
    # 測試文章 : Gossip 版 ， [花邊] 美國媒體對於籃網輪休感到不可思議 (NBA版中的文章)
   def test_Rule2_BoardExistsArticleNotBelongsToTheBoard(self):
        crawler(['-b', 'Gossip', '-a', 'M.1491980650.A.3ED'])
        filename = 'Gossip-M.1491980650.A.3ED.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            
            self.assertEqual(jsondata['error'], 'invalid url')
            
            # json 檔案內不存在正常情況下會出現的兩個 key : board && article_id
            self.assertTrue('board' not in jsondata)
            self.assertTrue('article_id' not in jsondata)
        os.remove(filename)
    # 測試情境 : 看板存在，且看板中存在該ID的文章 (Rule 3)
    # 測試文章 : NBA 版 ， [花邊] 美國媒體對於籃網輪休感到不可思議 (NBA版中的文章)
   def test_Rule3_BoardExistsArticleBelongsToTheBoard(self):
        crawler(['-b', 'NBA', '-a', 'M.1491980650.A.3ED'])
        filename = 'NBA-M.1491980650.A.3ED.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
            # 以文章的 (作者、ip、發文時間) 為 unique 的 data，驗證 crawler 得到的文章的正確性
            self.assertEqual(jsondata['author'], 'jay0601zzz (油頭胡志強)')
            self.assertEqual(jsondata['ip'], '111.83.123.106')
            self.assertEqual(jsondata['date'], 'Wed Apr 12 15:04:08 2017')
            
            # 再次驗證 input 與 crawler 得到的相同
            self.assertEqual(jsondata['board'], 'NBA')
            self.assertEqual(jsondata['article_id'], 'M.1491980650.A.3ED')
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()