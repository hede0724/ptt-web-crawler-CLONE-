import unittest
import sys
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os
from io import StringIO

class TestCrawlerByBoundaryValueTest(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
    def test_getLastPageMaximumPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(LastIndex+1)])           #Last+1,    Last+1
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(sys.stdout.getvalue(),'Processing index: '+str(LastIndex+1)+'\ninvalid url: https://www.ptt.cc/bbs/Aviation/index'+str(LastIndex+1)+'.html\n')
        os.remove(filename)
    def test_getLastPageMaximum(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex), str(LastIndex)])           #Last,    Last
        filename = 'Aviation-'+str(LastIndex)+'-'+str(LastIndex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertNotEqual(len(data['articles']),0)                    #NotEqual  while startIndex=LastPage length will not be 0 
        os.remove(filename)
       
    def test_robust_MaximumValuePlus2(self):          #May need to change Output while it should be in case of Index Out of range
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+2), str(LastIndex)])           #Last+2,    Last
        filename = 'Aviation-'+str(LastIndex+2)+'-'+str(LastIndex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        os.remove(filename)
        crawler(['-b', 'Aviation', '-i', str(LastIndex+2), str(LastIndex+1)])           #Last+2,    Last+1
        filename = 'Aviation-'+str(LastIndex+2)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        os.remove(filename)
        #crawler(['-b', 'Aviation', '-i', str(LastIndex), str(LastIndex+2)])           #Last,    Last+2
        #json.load有錯不知為啥
        
        #crawler(['-b', 'Aviation', '-i', '-1', str(LastIndex+2)])                       #-1,        Last+2
        #可能變全部都跑 可能要新改source code
        
        #crawler(['-b', 'Aviation', '-i', str(LastIndex+2), str(-1)])           #Last+2,    -1
        #沒生成檔案
        

    def test_robust_MaximumValuePlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(LastIndex+1)])       #Last+1,    Last+1
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        os.remove(filename)
        #crawler(['-b', 'Aviation', '-i', str(LastIndex+1), '-1'])                   #Last+1,    -1
        #沒有檔案
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(LastIndex+2)])           #Last+1,    Last+2
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(LastIndex+2)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        os.remove(filename)
        
        
    
        
    
        
if __name__ == '__main__':
    unittest.main()