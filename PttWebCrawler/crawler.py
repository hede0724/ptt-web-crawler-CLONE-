# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import re
import sys
import json
import requests
import argparse
import time
import codecs
from bs4 import BeautifulSoup
from six import u

__version__ = '1.0'

# if python 2, disable verify flag in requests.get()
VERIFY = True
if sys.version_info[0] < 3:
    VERIFY = False
    requests.packages.urllib3.disable_warnings()

class PttWebCrawler(object):
    """docstring for PttWebCrawler"""
    def __init__(self, cmdline=None):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
            A crawler for the web version of PTT, the largest online community in Taiwan.
            Input: board name and page indices (or articla ID)
            Output: BOARD_NAME-START_INDEX-END_INDEX.json (or BOARD_NAME-ID.json)
        ''')
        parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-i', metavar=('START_INDEX', 'END_INDEX'), type=int, nargs=2, help="Start and end index")
        group.add_argument('-a', metavar='ARTICLE_ID', help="Article ID")
        parser.add_argument('-p', metavar='PushNum',type=int , help="PushNum")
        parser.add_argument('-n',metavar='AuthorName',help = "AuthorName")
        parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
        
        if cmdline:
            args = parser.parse_args(cmdline)
        else:
            args = parser.parse_args()
        board = args.b
        PTT_URL = 'https://www.ptt.cc'
        if args.i:
            start = args.i[0]
            if args.i[1] == -1:
                end = self.getLastPage(board)
                #end = self.getLastPage(board)
            else:
                end = args.i[1]
                #end = args.i[1]
            index = start
            filename = board + '-' + str(start) + '-' + str(end) + '.json'
            AuthorName = args.n
            PushNum = args.p
            #print('AuthorName=',AuthorName)
            #print('pushNum=',PushNum)
            self.store(filename, u'{"articles": [', 'w')
            if(self.InputIsValid(start,end,board,self.getLastPage(board))):
                for i in range(end-start+1):
                    index = start + i
                    print('Processing index:', str(index))
                    resp = requests.get(
                        url=PTT_URL + '/bbs/' + board + '/index' + str(index) + '.html',
                        cookies={'over18': '1'}, verify=VERIFY
                    )
                    if resp.status_code != 200:
                        print('invalid url:', resp.url)
                        continue
                    soup = BeautifulSoup(resp.text)
                    divs = soup.find_all("div", "r-ent")
                    for div in divs:
                        try:
                            # ex. link would be <a href="/bbs/PublicServan/M.1127742013.A.240.html">Re: [問題] 職等</a>
                            href = div.find('a')['href']
                            link = PTT_URL + href
                            article_id = re.sub('\.html', '', href.split('/')[-1])
                            if(((args.p and (self.getPush(link, article_id, board) > PushNum)) or not args.p) and ((args.n and self.isEqualWithName(link, article_id, board,AuthorName)) or not args.n)):
                                    if div == divs[-1] and i == end-start:  # last div of last page
                                        self.store(filename, self.parse(link, article_id, board), 'a')
                                    else:
                                        self.store(filename, self.parse(link, article_id, board) + ',', 'a')
                        except:
                            pass
                    time.sleep(0.1)
            self.store(filename, u']}', 'a')            
        else:  # args.a
            article_id = args.a
            link = PTT_URL + '/bbs/' + board + '/' + article_id + '.html'
            filename = board + '-' + article_id + '.json'
            self.store(filename, self.parse(link, article_id, board), 'w')

    @staticmethod
    def parse(link, article_id, board):
        print('Processing article:', article_id)
        resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)
        if resp.status_code != 200:
            print('invalid url:', resp.url)
            return json.dumps({"error": "invalid url"}, sort_keys=True, ensure_ascii=False)
        soup = BeautifulSoup(resp.text)
        main_content = soup.find(id="main-content")
        metas = main_content.select('div.article-metaline')
        author = ''
        title = ''
        date = ''
        if metas:
            author = metas[0].select('span.article-meta-value')[0].string if metas[0].select('span.article-meta-value')[0] else author
            title = metas[1].select('span.article-meta-value')[0].string if metas[1].select('span.article-meta-value')[0] else title
            date = metas[2].select('span.article-meta-value')[0].string if metas[2].select('span.article-meta-value')[0] else date

            # remove meta nodes
            for meta in metas:
                meta.extract()
            for meta in main_content.select('div.article-metaline-right'):
                meta.extract()

        # remove and keep push nodes
        pushes = main_content.find_all('div', class_='push')
        for push in pushes:
            push.extract()

        try:
            ip = main_content.find(text=re.compile(u'※ 發信站:'))
            ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ip).group()
        except:
            ip = "None"

        # 移除 '※ 發信站:' (starts with u'\u203b'), '◆ From:' (starts with u'\u25c6'), 空行及多餘空白
        # 保留英數字, 中文及中文標點, 網址, 部分特殊符號
        filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
        expr = re.compile(u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, '', filtered[i])

        filtered = [_f for _f in filtered if _f]  # remove empty strings
        filtered = [x for x in filtered if article_id not in x]  # remove last line containing the url of the article
        content = ' '.join(filtered)
        content = re.sub(r'(\s)+', ' ', content)
        # print 'content', content

        # push messages
        p, b, n = 0, 0, 0
        messages = []
        for push in pushes:
            if not push.find('span', 'push-tag'):
                continue
            push_tag = push.find('span', 'push-tag').string.strip(' \t\n\r')
            push_userid = push.find('span', 'push-userid').string.strip(' \t\n\r')
            # if find is None: find().strings -> list -> ' '.join; else the current way
            push_content = push.find('span', 'push-content').strings
            push_content = ' '.join(push_content)[1:].strip(' \t\n\r')  # remove ':'
            push_ipdatetime = push.find('span', 'push-ipdatetime').string.strip(' \t\n\r')
            messages.append( {'push_tag': push_tag, 'push_userid': push_userid, 'push_content': push_content, 'push_ipdatetime': push_ipdatetime} )
            if push_tag == u'推':
                p += 1
            elif push_tag == u'噓':
                b += 1
            else:
                n += 1

        # count: 推噓文相抵後的數量; all: 推文總數
        message_count = {'all': p+b+n, 'count': p-b, 'push': p, 'boo': b, "neutral": n}

        # print 'msgs', messages
        # print 'mscounts', message_count

        # json data
        data = {
            'board': board,
            'article_id': article_id,
            'article_title': title,
            'author': author,
            'date': date,
            'content': content,
            'ip': ip,
            'message_conut': message_count,
            'messages': messages
        }
        # print 'original:', d
        return json.dumps(data, sort_keys=True, ensure_ascii=False)
    @staticmethod
    def Stub_getLastPage(board):
        return 10
    def Stub_isEqualWithName(link, article_id, board,AuthorName):
        return True
    def Stub_getPush(link, article_id, board):
        return 51
    
    @staticmethod
    def InputIsValid(start,end,board,last):
        
        if(start <= last and start >= 0 and end <= last and end >= 0):
            return True
        else:
            if((start > last or start < 0) and (end > last or end < 0)):
                print('Invalid startIndex and endIndex')
                return False
            elif((start > last or start < 0)):
                print('Invalid startIndex')
                return False
            else:
                print('Invalid endIndex')
                return False
            
    
    @staticmethod
    def isEqualWithName(link, article_id, board,AuthorName):
        resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)
        soup = BeautifulSoup(resp.text)
        main_content = soup.find(id="main-content")
        metas = main_content.select('div.article-metaline')
        author = ''
        title = ''
        date = ''
        if metas:
            author = metas[0].select('span.article-meta-value')[0].string if metas[0].select('span.article-meta-value')[0] else author
        print('authorName',author)
        if(AuthorName is author):
            return True
        else:
            return False
            
    @staticmethod
    def getPush(link, article_id, board):
        resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)
        soup = BeautifulSoup(resp.text)
        main_content = soup.find(id="main-content")
        pushes = main_content.find_all('div', class_='push')
        for push in pushes:
            push.extract()
        p = 0
        for push in pushes:
            if not push.find('span', 'push-tag'):
                continue
            push_tag = push.find('span', 'push-tag').string.strip(' \t\n\r')
            if push_tag == u'推':
                p += 1
        return p    
        
    @staticmethod
    def getLastPage(board):
        content = requests.get(
            url= 'https://www.ptt.cc/bbs/' + board + '/index.html',
            cookies={'over18': '1'}
        ).content.decode('utf-8')
        first_page = re.search(r'href="/bbs/' + board + '/index(\d+).html">&lsaquo;', content)
        if first_page is None:
            return 1
        return int(first_page.group(1)) + 1

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def get():
        with codecs.open(filename, mode, encoding='utf-8') as f:
            j = json.load(f)
            print(f)
            
    @staticmethod
    def get_author_name(board, author):
        PTT_URL = 'https://www.ptt.cc'
        _filename = board + '-' + author + '.json'
    
        LastIndex = PttWebCrawler.getLastPage(board)
        PttWebCrawler(['-b', board, '-i', str(0), str(LastIndex)])
        filename = board+'-'+str(0)+'-'+str(LastIndex)+'.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        num = 0
        for _article in data['articles']:
            if author == _article['author']:
                link = PTT_URL + '/bbs/' + board + '/' + _article['article_id'] + '.html'
                num = num + 1
        return num
        
if __name__ == '__main__':
    c = PttWebCrawler.get_author_name('NCTU_TALK', 'NCTUbigGG (交大大GG)')