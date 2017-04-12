import unittest
import sys
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os
from io import StringIO

class TestCrawlerByBoundaryValueTest(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
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
            #self.assertEqual(len(data['articles']),11)
            self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
    def test_crawler_StartIndexMinimumValue(self):
        crawler(['-b', 'NBA', '-i', '0', '0'])
        filename = 'NBA-0-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertNotEqual(len(data['articles']),0)                    #NotEqual  while startIndex=LastPage length will not be 0 
            #self.assertEqual(len(data['articles']),11)
        os.remove(filename)
        
    def test_crawler_StartIndexMinimumValuePlus(self):
        crawler(['-b', 'NBA', '-i', '1', '0'])
        filename = 'NBA-1-0.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data['articles']),0)
        os.remove(filename)
    def test_getLastPageMaximumPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(LastIndex+1)])           #Last+1,    Last+1
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        #self.assertEqual(sys.stdout.getvalue(),'Processing index: '+str(LastIndex+1)+'\ninvalid url: https://www.ptt.cc/bbs/Aviation/index'+str(LastIndex+1)+'.html\n')
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex and endIndex\n')
        os.remove(filename)
        
    def test_getLastPageMaximum(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex), str(LastIndex)])           #Last,    Last
        filename = 'Aviation-'+str(LastIndex)+'-'+str(LastIndex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertNotEqual(len(data['articles']),0)                    #NotEqual  while startIndex=LastPage length will not be 0 
        os.remove(filename)
       
    

    def test_robust_MaximumValuePlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(LastIndex+1)])       #Last+1,    Last+1
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex and endIndex\n')
        os.remove(filename)
        
    
        
    def test_robust_MaxPlus1_Minus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), '-1'])                   #Last+1,    -1
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(-1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
    def test_robust_MaxPlus1_Minus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), '0'])                   #Last+1,    0
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(0)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
    def test_robust_MaxPlus1_halfMax(self):
        LastIndex = crawler.getLastPage('Aviation')
        endindex = int(LastIndex/2)
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(endindex)])                   #Last+1,    Last/2
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(endindex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
    def test_robust_MaxPlus1_Max(self):
        LastIndex = crawler.getLastPage('Aviation')
        endindex = int(LastIndex)
        crawler(['-b', 'Aviation', '-i', str(LastIndex+1), str(endindex)])                   #Last+1,    Last
        filename = 'Aviation-'+str(LastIndex+1)+'-'+str(endindex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex\n')
        os.remove(filename)
        
        
        
    def test_robust_Minus1_MaxPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(-1), str(LastIndex+1)])           #-1,    Last+1
        filename = 'Aviation-'+str(-1)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid startIndex and endIndex\n')
        os.remove(filename)
        
    def test_robust_zero_MaxPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        crawler(['-b', 'Aviation', '-i', str(0), str(LastIndex+1)])           #0,    Last+1
        filename = 'Aviation-'+str(0)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid endIndex\n')
        os.remove(filename)
    def test_robust_halfMax_MaxPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        startindex = int(LastIndex/2)
        crawler(['-b', 'Aviation', '-i', str(startindex), str(LastIndex+1)])           #Last/2,    Last+1
        filename = 'Aviation-'+str(startindex)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid endIndex\n')
        os.remove(filename)
    def test_robust_Max_MaxPlus1(self):
        LastIndex = crawler.getLastPage('Aviation')
        startindex = int(LastIndex)
        crawler(['-b', 'Aviation', '-i', str(startindex), str(LastIndex+1)])           #Last,    Last+1
        filename = 'Aviation-'+str(startindex)+'-'+str(LastIndex+1)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data['articles']),0)
        self.assertEqual(sys.stdout.getvalue(),'Invalid endIndex\n')
        os.remove(filename)
    
    def test_normal_zero_Max(self):
        LastIndex = crawler.getLastPage('NTU-CHKongFu')
        crawler(['-b', 'NTU-CHKongFu', '-i', str(0), str(LastIndex)])           #0,    Last
        filename = 'NTU-CHKongFu-'+str(0)+'-'+str(LastIndex)+'.json'
        with codecs.open(filename,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.assertNotEqual(len(data['articles']),0)                    #NotEqual  while startIndex=LastPage length will not be 0 
        os.remove(filename)
    
        
if __name__ == '__main__':
    unittest.main()