# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# -*- codeing = utf-8 -*-
# @Time : 2020/12/1 18:36
# @Author : 招财进宝
# @File : spiderW.py
# @Software: PyCharm

import requests
from lxml import etree
import time
import random
import pandas as pd
import sqlite3

order = ['totalrank', 'click', 'pubdate', 'dm', 'stow']
duration = [1, 2, 3, 4]
# tid = [0, 1, 13, 167, 3, 129, 4, 36, 188, 234, 223, 160, 211, 217, 119, 155, 202, 5, 181, 177]

tid = ['1&tids_2=24', '1&tids_2=25', '1&tids_2=47', '1&tids_2=210', '1&tids_2=86', '1&tids_2=27', 
       '13',
       '167', 
       '3&tids_2=28', '3&tids_2=31', '3&tids_2=30', '3&tids_2=194', '3&tids_2=59', '3&tids_2=193','3&tids_2=29','3&tids_2=130', 
       '129&tids_2=20', '129&tids_2=198', '129&tids_2=199', '129&tids_2=200', '129&tids_2=154','129&tids_2=156', 
       '4&tids_2=17', '4&tids_2=171','4&tids_2=172', '4&tids_2=65', '4&tids_2=173', '4&tids_2=121', '4&tids_2=136',
       '36&tids_2=201', '36&tids_2=124', '36&tids_2=228', '36&tids_2=207', '36&tids_2=208', '36&tids_2=209','36&tids_2=229','36&tids_2=122', 
       '188', 
       '234', 
       '223', 
       '160&tids_2=138', '160&tids_2=239', '160&tids_2=161', '160&tids_2=162','160&tids_2=21', 
       '211&tids_2=76', '211&tids_2=212', '211&tids_2=213', '211&tids_2=215',
       '217&tids_2=218', '217&tids_2=219','217&tids_2=220', '217&tids_2=221', '217&tids_2=222', '217&tids_2=75', 
       '119&tids_2=22', '119&tids_2=26','119&tids_2=126', '119&tids_2=216', '119&tids_2=127', 
       '155',
       '5&tids_2=71', '5&tids_2=241', '5&tids_2=242','5&tids_2=137', 
       '181&tids_2=182', '181&tids_2=183', '181&tids_2=85', '181&tids_2=184', 
       '177']

AllTag = ['嘉然','向晚','贝拉','珈乐','乃琳','嘉心糖', '嘉然今天吃什么', 'A-SOUL', '传说的世界',  '向晚大魔王', '顶晚人', '乃琳Queen',  '乃淇琳',
          '贝拉kira', '贝极星',  '珈乐Carol', 'asoul', 'GNK48']

def modify_list(list, zh):
    i = 0
    while i < len(list):
        if list[i] == zh:
            return list[i:len(list)]
        i = i + 1
    return list

def sql():
    conn = sqlite3.connect('ASOUL.db')
    print("数据库打开成功")
    c = conn.cursor()
    c.execute('''CREATE TABLE ASOUL_ALL
           (video_url BLOB PRIMARY KEY     NOT NULL UNIQUE,
           title           BLOB    NOT NULL,
           region            BLOB     NOT NULL,
           view_num        BLOB     NOT NULL,
           upload_time       BLOB   NOT NULL,
           up_author    BLOB   NOT NULL,
           tags    BLOB  NOT NULL,
           danmu    BLOB   NOT NULL);''')
    print("数据表创建成功")
    conn.commit()

def test_sql():
    conn = sqlite3.connect('ASOUL.db')
    print("数据库打开成功")
    c = conn.cursor()
    cursor = c.execute("SELECT video_url, title, tags, view_num  from ASOUL_ALL")
    for row in cursor:
        print
        "ID = ", row[0]
        print
        "NAME = ", row[1]
        print
        "ADDRESS = ", row[2]
        print
        "SALARY = ", row[3], "\n"

    print("数据操作成功")

def Xhttps():
    f = open("https.txt", "r")
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


newIter = Xhttps()
AllTag = modify_list(AllTag, newIter[0])
order = modify_list(order, newIter[1])
duration = modify_list(duration, newIter[3])
tid = modify_list(tid, newIter[4])


def get_target():

    conn = sqlite3.connect('ASOUL.db')
    print("数据库打开成功")
    c = conn.cursor()
    f = open("https.txt","r+")
    for keyword in AllTag:
        for iorder in order:
            result = pd.DataFrame()
            for iduration in duration:
                for itid in tid:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

                    url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&order={}&duration={}&tids_1={}'.format(
                        keyword, iorder, iduration, itid)
                    html = requests.get(url, headers=headers)
                    bs = etree.HTML(html.text)
                    result = '10'
                    if bs.xpath('//li[@class="page-item last"]//text()'):
                        result = bs.xpath('//li[@class="page-item last"]//text()')[0].strip('\n        ')

                    print("page: " + result)
                    page = int(result)

                    for i in range(1, page):
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

                        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}&order={}&duration={}&tids_1={}'.format(keyword, i, iorder, iduration, itid)
                        html = requests.get(url.format(i), headers=headers)
                        bs = etree.HTML(html.text)
                        items = bs.xpath('//li[@class = "video-item matrix"]')
                        f.write(url.format(i))
                        f.seek(0,0)
                        for item in items:
                            video_url = item.xpath('div[@class = "info"]/div/a/@href')[0].replace("//", "")  # 每个视频的来源地址
                            title = item.xpath('div[@class = "info"]/div/a/@title')[0]  # 每个视频的标题
                            region = item.xpath('div[@class = "info"]/div[1]/span[1]/text()')[0].strip('\n        ')  # 每个视频的分类版块如动画
                            view_num = item.xpath('div[@class = "info"]/div[3]/span[1]/text()')[0].strip('\n        ')  # 每个视频的播放量
                            danmu = item.xpath('div[@class = "info"]/div[3]/span[2]/text()')[0].strip('\n        ')  # 弹幕
                            upload_time = item.xpath('div[@class = "info"]/div[3]/span[3]/text()')[0].strip('\n        ')  # 上传日期
                            up_author = item.xpath('div[@class = "info"]/div[3]/span[4]/a/text()')[0].strip('\n        ')  # up主

                            html2 = requests.get('https://' + video_url)
                            bs2 = etree.HTML(html2.text)
                            items2 = bs2.xpath('//meta[@name="keywords"]/@content') # 取tag
                            items3 = items2[0].split(',')
                            items4 = items3[1:len(items3)]

                            print(title)
                            if set(AllTag) & set(items4):

                                c.execute("INSERT OR IGNORE INTO ASOUL_ALL VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                          (str('https://' + video_url), str(title), str(region), str(view_num), str(upload_time), str(up_author), str(items2), str(danmu)))

                                '''
                                df = pd.DataFrame(
                                    {'title': [title], 'region': [region], 'view_num': [view_num], 'danmu': [danmu],
                                     'upload_time': [upload_time], 'up_author': [up_author], 'video_url': [video_url],
                                     'tags': [items4]})
                                print(df)
                                result = pd.concat([result, df])
                                '''

                        time.sleep(random.random()/2 + 0.6)
                        print('TAG:{} order:{} duration:{} tid:{} 已经完成b站第 {} 页爬取'.format(keyword, iorder, iduration, itid, i))
                        conn.commit()
                        print("commit success")
            '''
            result = result.drop_duplicates(subset='video_url')  # 按视频地址去重
            saveName = keyword + "_" + iorder +".csv"
            result.to_csv(saveName, encoding='utf-8-sig', index=False)  # 保存为csv格式的文件
            '''
    f.close()
    c.close()
    return 'success'


if __name__ == "__main__":
#    sql()
    while True:
        if get_target() == 'success':
            break
        time.sleep(60)
        print('sleep 60 sec')

    print("all success")



# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
