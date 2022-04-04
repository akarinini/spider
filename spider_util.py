import sqlite3
import requests
from lxml import etree
import itertools
import goto
from goto import with_goto
from dominate.tags import label
import time
from fake_useragent import UserAgent
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}

proxies = {
    'https': 'https://user:password123@124.223.8.236:8888',
    'http': 'http://user:password123@124.223.8.236:8888'
}

bili_xpath = {'video': '//li[@class = "video-item matrix"]',
              'video_url': 'div[@class = "info"]/div/a/@href',
              'title': 'div[@class = "info"]/div/a/@title',
              'region': 'div[@class = "info"]/div[1]/span[1]/text()',
              'view_num': 'div[@class = "info"]/div[3]/span[1]/text()',
              'danmu': 'div[@class = "info"]/div[3]/span[2]/text()',
              'upload_time': 'div[@class = "info"]/div[3]/span[3]/text()',
              'up_author': 'div[@class = "info"]/div[3]/span[4]/a/text()',
              'url': 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}&order={}&duration={}&tids_1={}',
              'page': '//li[@class="page-item last"]//text()',
              'page_2': '//li[@class="page-item"]',
              'tag': '//meta[@name="keywords"]/@content',
              'author_uid': '//span[@title="up主"]/a/@href',
              'author_name': '//span[@title="up主"]/a//text()',
              'user_list': '//div[@id="user-list"]//li[@class="user-item"]',
              'user_uid': '//div[@class="headline"]/a[@class="title"]/@href',
              'user_name': '//div[@class="headline"]/a[@class="title"]//text()',
              'space_page': '//div[@id="page-video"]'}


wait_time = 181


def get_all_video_space():
    url = 'http://api.bilibili.com/x/space/arc/search?mid=672328094&pn=1&ps=25&jsonp=jsonp'
    # 访问url
    r = requests.get(url, proxies=proxies)
    # 将爬取道德json格式的数据转化为字典
    text = json.loads(r.text)
    print(text)
    # 取出嵌套字典里我们想要的部分
    # 这里的字典嵌套在控制台里其实看的很清楚，我在上面的截图里圈了出来
    res = text['data']['list']['vlist']
    for item in res:
        # 以列表的形式取出对我们有用的数据
        list = ['av: ' + str(item['aid']), ' 视频标题: ' + item['title'], ' 播放量: ' + str(item['play']),
                ' 评论条数: ' + str(item['video_review'])]
        # 转化为字符串格式
        result = ''.join(list)
        # 写进文件里
        with open('wlg.txt', 'a+', encoding="utf-8") as f:
            f.write(result + '\n')


@with_goto
def get_space_video_by_api(url):
    # 访问url
    label.begin
    r = requests.get(url, headers)
    # 将爬取道德json格式的数据转化为字典
    text = json.loads(r.text)
    code = text['code']
    if code == 0:
        return text
    elif code == 16001:
        print('该频道尚不存在')
        return {'code': 16001, 'message': '稿件不可见', 'ttl': 1}
    elif code == 62002:
        print({'code': 62002, 'message': '稿件不可见', 'ttl': 1})
        return {'code': 62002, 'message': '稿件不可见', 'ttl': 1}
    elif code == -404:
        print({'code': -404, 'message': '啥都木有', 'ttl': 1})
        return {'code': -404, 'message': '啥都木有', 'ttl': 1}
    else:
        print(text)
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto.begin


@with_goto
def parse_bili_xpath(node_string, url):
    result = []
    label .begin
    try:
        html = requests.get(url, headers=headers)
        bs = etree.HTML(html.text)
        result = bs.xpath(node_string)
    except Exception as e:
        print('parse_bili_xpath Error: %s' % e)
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin
    if result:
        return result
    else:
        print('parse_bili_xpath result is null list')
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin

@with_goto
def parse_author_xpath(author_uid, author_name, url):
    result = []
    label .begin
    try:
        html = requests.get(url, headers=headers)
        bs = etree.HTML(html.text)
        result = bs.xpath(author_uid)
        result2 = bs.xpath(author_name)
    except Exception as e:
        print('parse_bili_xpath Error: %s' % e)
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin
    if result:
        return [result, result2]
    else:
        print('parse_author_xpath result is null list')
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin


@with_goto
def parse_bili_page_xpath(node_string, url):
    result = []
    label .begin
    try:
        html = requests.get(url, headers=headers)
        bs = etree.HTML(html.text)
        result = bs.xpath(node_string)
    except Exception as e:
        print('parse_bili_page_xpath Error: %s' % e)
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin
    return result

@with_goto
def parse_bili_author_xpath(url):
    bs = []
    label .begin
    try:
        html = requests.get(url, headers=headers)
        bs = etree.HTML(html.text)
    except Exception as e:
        print('parse_bili_page_xpath Error: %s' % e)
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto .begin
    if len(bs):
        return bs
    else:
        print('parse_bili_author_xpath result is null list')
        for item in range(wait_time, 0, -1):
            print("\rTime remains {} sec".format(item), end="", flush=True)
            time.sleep(1)
        goto.begin


def item_xpath(item, node_string):
    try:
        tmp = item.xpath(node_string)
    except Exception as e:
        print('item_xpath Error: %s' % e)
        return []
    return tmp

def spider_print(keyword, iorder, iduration, itid, *page):
    if page:
        print('Tag: {}, order: {}, duration: {}, tid: {}, page nums = {}'.format(keyword, iorder, iduration, itid, page[0]))
    else:
        print('Tag: {}, order: {}, duration: {}, tid: {}'.format(keyword, iorder, iduration, itid))



def parse_tags(item):
    tmp = item[0].split(',')
    return tmp[1:len(tmp)]

def parse_https_txt():
    f = open("https.txt", "r", encoding='UTF-8')
    all = f.readline().split('&')
    keyword = all[0].split('?')[1].split('=')[1]
    order = all[3].split('=')[1]
    page = all[2].split('=')[1]
    duration = all[4].split('=')[1]
    tid = all[5].split('=')[1]
    f.close()
    if len(all) == 6:
        return [keyword, order, page, duration, tid]
    else:
        return [keyword, order, page, duration, tid + '&' + all[6]]


def sql_connect():
    conn = sqlite3.connect('/home/ubuntu/python/ASOUL.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE ASOUL_ALL
                   (video_url BLOB PRIMARY KEY     NOT NULL UNIQUE,
                   title           BLOB    NOT NULL,
                   region            BLOB     NOT NULL,
                   view_num        BLOB     NOT NULL,
                   upload_time       BLOB   NOT NULL,
                   up_author    BLOB   NOT NULL,
                   tags    BLOB  NOT NULL,
                   danmu    BLOB   NOT NULL);''')
    except Exception as e:
        print('sql_connect Error: %s' % e)
        print('no need to create ASOUL_ALL table')
    try:
        c.execute('''CREATE TABLE ASOUL_ALL_API
                   (video_url BLOB PRIMARY KEY     NOT NULL UNIQUE,
                   title           BLOB    NOT NULL,
                   region            BLOB     NOT NULL,
                   view_num        BLOB     NOT NULL,
                   upload_time       BLOB   NOT NULL,
                   up_author    BLOB   NOT NULL,
                   tags    BLOB  NOT NULL,
                   danmu    BLOB   NOT NULL,
                   aid    BLOB  NOT NULL,
                   comment    BLOB  NOT NULL,
                   copyright    BLOB  NOT NULL,
                   length    BLOB  NOT NULL,
                   bvid    BLOB  NOT NULL);''')
    except Exception as e:
        print('sql_connect Error: %s' % e)
        print('no need to create ASOUL_ALL_API table')
    try:
        c.execute('''CREATE TABLE AUTHOR_UID
                   (up_author_uid BLOB PRIMARY KEY     NOT NULL UNIQUE,
                   up_author           BLOB    NOT NULL);''')
    except Exception as e:
        print('sql_connect Error: %s' % e)
        print('no need to create AUTHOR_UID table')
    return conn

test_url = 'https://search.bilibili.com/all?keyword=贝拉&from_source=nav_suggest_new0&page=4&order=totalrank&duration=0&tids_1=13'
test_url2 = 'https://search.bilibili.com/all?keyword=嘉然今天吃什么'
test_baidu = 'http://www.baidu.com/'
if __name__ == "__main__":
    url = 'http://api.bilibili.com/x/space/arc/search?mid=672328094&pn=1&ps=25&jsonp=jsonp'
    html = requests.get(test_url2, proxies=proxies, verify=False)
    bs = etree.HTML(html.text)

    print(bs.xpath('//meta'))
    result = bs.xpath(bili_xpath['author_uid'])
    result2 = bs.xpath(bili_xpath['author_name'])
    print(len(result))
    for iter in range(0, len(result) - 1):
        print(result2[iter])
        if result2[iter].strip('\n        ') == '嘉然今天吃什么':
            print(result[iter].replace("//", "").split('/')[1].split('?')[0])
            break
    # get_all_video_space()
    print('1')
