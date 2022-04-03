import time
from fnmatch import fnmatch

import requests
from lxml import etree

import spider_util
import sql_util
import itertools
import random
import goto
from goto import with_goto

# , 'click', 'pubdate', 'dm', 'stow'
order = ['totalrank']

duration = ['0']
duration_all = ['1', '2', '3', '4']
tid_all_search = ['1&tids_2=25', '1&tids_2=47', '1&tids_2=27','3&tids_2=31',
                '3&tids_2=130','129&tids_2=154','4&tids_2=17', '4&tids_2=171', 
                '4&tids_2=172', '4&tids_2=65','160&tids_2=138','160&tids_2=21']

tid = ['1',#'1&tids_2=24', '1&tids_2=25', '1&tids_2=47', '1&tids_2=210', '1&tids_2=86', '1&tids_2=27',
       '13',
       '167', 
       '3', #&'3tids_2=28', '3&tids_2=31', '3&tids_2=30', '3&tids_2=194', '3&tids_2=59', '3&tids_2=193', '3&tids_2=29', '3&tids_2=130',
       '129', #'129&tids_2=20', '129&tids_2=198', '129&tids_2=199', '129&tids_2=200', '129&tids_2=154', '129&tids_2=156',
       '4', #'4&tids_2=17', '4&tids_2=171', '4&tids_2=172', '4&tids_2=65', '4&tids_2=173', '4&tids_2=121', '4&tids_2=136',
       '36', #&tids_2=201', '36&tids_2=124', '36&tids_2=228', '36&tids_2=207', '36&tids_2=208', '36&tids_2=209', '36&tids_2=229', '36&tids_2=122',  # url的链接到这里会出问题
       '188',
       '234',
       '223',
       '160', #'160&tids_2=138', '160&tids_2=239', '160&tids_2=161', '160&tids_2=162', '160&tids_2=21',
       '211', #&tids_2=76', '211&tids_2=212', '211&tids_2=213', '211&tids_2=215',
       '217', #&tids_2=218', '217&tids_2=219', '217&tids_2=220', '217&tids_2=221', '217&tids_2=222', '217&tids_2=75',
       '119', #&tids_2=22', '119&tids_2=26', '119&tids_2=126', '119&tids_2=216', '119&tids_2=127',
       '155',
       '5', #&tids_2=71', '5&tids_2=241', '5&tids_2=242', '5&tids_2=137',
       '181', #&tids_2=182', '181&tids_2=183', '181&tids_2=85', '181&tids_2=184',
       '177']
# 0 duration further search
tid_further_search = ['1&tids_2=24','1&tids_2=210','1&tids_2=86','3tids_2=28','3&tids_2=30',
        '3&tids_2=194','3&tids_2=59','3&tids_2=193','3&tids_2=29','129&tids_2=20',
        '129&tids_2=198','129&tids_2=199','129&tids_2=200','129&tids_2=156',
        '4&tids_2=173', '4&tids_2=121', '4&tids_2=136','160&tids_2=239', '160&tids_2=161', '160&tids_2=162']

AllTag = ['嘉然', '向晚', '贝拉', '珈乐', '乃琳', 'asoul']#, '嘉心糖', '嘉然今天吃什么', 'A-SOUL', '传说的世界', '向晚大魔王', '顶晚人', '乃琳Queen', '乃淇琳',
        #  '贝拉kira', '贝极星', '珈乐Carol', 'asoul', 'GNK48']
AllTag2 = ['嘉然', '向晚', '贝拉', '珈乐', '乃琳', '阿草', '嘉心糖', '嘉然今天吃什么', 'A-SOUL', '传说的世界', '向晚大魔王', '顶晚人', '乃琳Queen', '乃淇琳',
         '贝拉kira', '贝极星', '珈乐Carol', 'asoul', 'GNK48', '超级敏感', '传说的世界', 'A-SOUL二创激励计划']

url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}&order={}&duration={}&tids_1={}'

def start_spider(AllTag, order, duration, tid):
    # connect SqlLite
    c = spider_util.sql_connect()
    # read last https to get [keyword, order, page, duration, tid]
    last_itertion = spider_util.parse_https_txt()
    print(last_itertion)

    f_https = open("https.txt", "r+", encoding='UTF-8')
    f_log = open("log.txt", "r+", encoding='UTF-8')

    DING = False
    DING_PAGE = False

    for item in itertools.product(AllTag, order, duration, tid):
        print('itertion: ' + item[0] + ' ' + item[1] + ' ' + item[2] + ' ' + item[3])
        q1 = (last_itertion[0] == item[0])
        q2 = (last_itertion[1] == item[1])
        q3 = (last_itertion[3] == item[2])
        q4 = (last_itertion[4] == item[3])
        if q1 and q2 and q3 and q4:
            DING = True        

        if DING:
            # get page nums, firstly get the page node
            page = spider_util.parse_bili_page_xpath(spider_util.bili_xpath['page'], url.format(item[0], 1, item[1], item[2], item[3]))
            # sleep 0.6 sec
            time.sleep(random.random() / 10 + 0.6)
            if page: # if page nums < 10, bilibili do not have max page nums node
                page = page[0].strip('\n        ')
                spider_util.spider_print(item[0], item[1], item[2], item[3], page)
            else:
                page = len(spider_util.parse_bili_page_xpath(spider_util.bili_xpath['page_2'], url.format(item[0], 1, item[1], item[2], item[3]))) + 1
                # sleep 0.6 sec
                time.sleep(random.random() / 10 + 0.6)
                print('no max page node, so page = {}'.format(page))
                spider_util.spider_print(item[0], item[1], item[2], item[3], page)

            for i in range(1, int(page)):
                if i == int(last_itertion[2]):
                    DING_PAGE = True
                if DING_PAGE:
                    f_https.write(url.format(item[0], i, item[1], item[2], item[3]))
                    f_log.write(url.format(item[0], i, item[1], item[2], item[3]))
                    f_https.seek(0, 0)
                    # get each video path
                    print(url.format(item[0], i, item[1], item[2], item[3]))
                    items = spider_util.parse_bili_xpath(spider_util.bili_xpath['video'], url.format(item[0], i, item[1], item[2], item[3]))
                    # sleep 0.6 sec
                    time.sleep(random.random() / 10 + 0.6)
                    # each video path used to parse
                    for item2 in items:
                        video_url = spider_util.item_xpath(item2, spider_util.bili_xpath['video_url'])[0].replace("//", "")
                        title = spider_util.item_xpath(item2, spider_util.bili_xpath['title'])[0]
                        region = spider_util.item_xpath(item2, spider_util.bili_xpath['region'])[0].strip('\n        ')
                        view_num = spider_util.item_xpath(item2, spider_util.bili_xpath['view_num'])[0].strip('\n        ')
                        danmu = spider_util.item_xpath(item2, spider_util.bili_xpath['danmu'])[0].strip('\n        ')
                        upload_time = spider_util.item_xpath(item2, spider_util.bili_xpath['upload_time'])[0].strip('\n        ')
                        up_author = spider_util.item_xpath(item2, spider_util.bili_xpath['up_author'])[0].strip('\n        ')
                        up_author_uid = spider_util.item_xpath(item2, spider_util.bili_xpath['author_uid'])[0].replace("//", "").split('/')[1].split('?')[0]

                        print('video_url: ' + video_url)
                        str_tag = spider_util.parse_bili_xpath(spider_util.bili_xpath['tag'], 'https://' + video_url)
                        # sleep 0.6 sec
                        time.sleep(random.random()/10 + 0.6)
                        tag = str_tag[0].split(',')
                        tag = tag[1:len(tag)]

                        if set(AllTag2) & set(tag):
                            c.execute("INSERT OR IGNORE INTO ASOUL_ALL VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (str('https://' + video_url), str(title), str(region), str(view_num), str(upload_time), str(up_author), str(str_tag), str(danmu)))
                            c.execute("INSERT OR IGNORE INTO AUTHOR_UID VALUES (?, ?)",
                                      (str(up_author_uid), str(up_author)))

                    c.commit()
                    print('commit [TAG:{} order:{} duration:{} tid:{}] success! finish {} page'.format(item[0], item[1], item[2], item[3], i))
                else:
                    print("DING_PAGE is False, we should continue. Current page = {}".format(i))
                    continue
        else:
            print("DING is False, we should continue")
            continue
    f_https.close()
    f_log.close()
    c.close()


def get_author_uid():
    conn = sql_util.sql_connect()
    all = conn.cursor().execute("SELECT *  from AUTHOR_UID").fetchall()
    conn.close()
    re = []
    for iter in all:
        re.append(iter[1])
    set(re)
    author_name = sql_util.get_author_name()
    search_url = 'https://search.bilibili.com/upuser?keyword={}'
    c = spider_util.sql_connect()
    print('author nums = {}'.format(len(author_name)))
    f_name = open("names.txt", "r+", encoding='UTF-8')
    cur_name = f_name.readline()
    jishuqi = 0
    DING = False
    for i in author_name:

        jishuqi = jishuqi + 1
        print('i = {}, {} of {}, {}%'.format(i, jishuqi, len(author_name), jishuqi*100/len(author_name)))
        if i in re:
            print('{} in table'.format(i))
            continue
        else:
            print('no this user')
            f_name.write(i)
            f_name.write('\n')
            continue
        # sleep 0.6 sec
        time.sleep(random.random() / 10 + 0.6)
        # '//div[@class="error-wrap error-0"]/p[@class="text"]//text()',
        test_xpath = spider_util.parse_bili_author_xpath(search_url.format(i)).xpath('//div[@class="total-wrap"]/p[@class="total-text"]//text()')[0].strip('\n        ')

        if test_xpath == '共找到0个用户':
            print('no this user')
            f_name.write(i)
            f_name.write('\n')
            continue
        else:
            time.sleep(random.random() / 10 + 0.6)
            items = spider_util.parse_bili_xpath(spider_util.bili_xpath['user_list'], search_url.format(i))
            # items = spider_util.parse_bili_xpath(spider_util.bili_xpath['user_list'], 'https://space.bilibili.com/35459743?from=search')

            up_author = spider_util.item_xpath(items[0], spider_util.bili_xpath['user_name'])[0].strip('\n        ')

            print('i = {}   up_author = {}'.format(i, up_author))
            if up_author == i:
                up_author_uid = \
                    (spider_util.item_xpath(items[0], spider_util.bili_xpath['user_uid'])[0].replace("//", ""))

                print('up_author = {}, up_author_uid = {}'.format(up_author, up_author_uid))
                up_author_uid = up_author_uid.split('?')
                # print('up_author = {}, up_author_uid = {}'.format(up_author, up_author_uid))
                up_author_uid = up_author_uid[0].split('/')
                # print('up_author = {}, up_author_uid = {}'.format(up_author, up_author_uid))
                up_author_uid = up_author_uid[1]
                print('up_author = {}, up_author_uid = {}'.format(up_author, up_author_uid))
                c.execute("INSERT OR IGNORE INTO AUTHOR_UID VALUES (?, ?)",
                          (str(up_author_uid), str(up_author)))
                c.commit()
    f_name.close()
    c.close()

def get_video_user_space():
    c = spider_util.sql_connect()
    DING = False
    # space_url = 'https://space.bilibili.com/{}/video'
    # space_page_url = 'https://space.bilibili.com/{}/video?tid=0&page={}&keyword=&order=pubdate'
    f_name = open("uid.txt", "r+", encoding='UTF-8')
    cur_name = f_name.readline()
    f_name.close
    space_api = 'https://api.bilibili.com/x/space/arc/search?mid={}&pn={}&ps=50&jsonp=jsonp'
    uid = sql_util.get_user_uid()
    jishuqi = 0
    if cur_name:
        print('current name = {}'.format(cur_name))
    else:
        cur_name = uid[0]
    for i in uid:
        jishuqi = jishuqi + 1
        print('i = {}, {} of {}, {}%'.format(i, jishuqi, len(uid), jishuqi * 100 / len(uid)))
        if cur_name == i:
            DING = True
        if i == '1651422290':
            print('continue 1651422290')
            continue
        if DING:
            f_name = open("uid.txt", "w+", encoding='UTF-8')
            f_name.write(i)
            f_name.close
            print('uid: {}'.format(i))
            time.sleep(random.random() / 10 + 0.1)
            page = spider_util.get_space_video_by_api(space_api.format(i, 1))
            page_nums = int(page['data']['page']['count']/page['data']['page']['ps']) + 1
            print('space page nums: {}'.format(page_nums))
            for iter_page_nums in range(1, page_nums + 1):
                print('page_nums = {}, {} of {}, {}%'.format(page_nums, iter_page_nums, page_nums, iter_page_nums * 100 / page_nums))
                time.sleep(random.random() / 10 + 0.1)
                print(space_api.format(i, iter_page_nums))
                video = spider_util.get_space_video_by_api(space_api.format(i, iter_page_nums))
                res = video['data']['list']['vlist']
                for item in res:
                    # print(item)
                    bvid = str(item['bvid'])
                    title = str(item['title'])
                    view_num = str(item['play'])
                    region = str(item['typeid'])
                    danmu = str(item['video_review'])
                    up_author = str(item['author'])
                    upload_time = str(item['created'])
                    aid = str(item['aid'])
                    comment = str(item['comment'])
                    copyright = str(item['copyright'])
                    length = str(item['length'])

                    video_url = 'https://www.bilibili.com/video/{}?from=search'.format(bvid)
                    # sleep 0.6 sec
                    time.sleep(random.random() / 10 + 0.1)
                    # str_tag = spider_util.parse_bili_xpath(spider_util.bili_xpath['tag'], video_url)
                    # tag = str_tag[0].split(',')
                    # tag = tag[1:len(tag)]

                    tag_api = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={}'.format(aid)
                    str_tag = []
                    tag = spider_util.get_space_video_by_api(tag_api)
                    # print(len(tag['data']))
                    for itag in tag['data']:
                        # print(itag['tag_name'])
                        str_tag.append(itag['tag_name'])
                    print('mid:{}, bvid:{}, aid:{}'.format(i, bvid, aid))
                    print(set(AllTag2) & set(str_tag))
                    if set(AllTag2) & set(str_tag):
                        c.execute("INSERT OR IGNORE INTO ASOUL_ALL_API VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  (str(video_url), str(title), str(region), str(view_num), str(upload_time),
                                   str(up_author), str(str_tag), str(danmu), aid, comment, copyright, length, bvid))
                        print(video_url)
                        c.commit()
                        print('commit success')

                c.commit()
                print('commit success')
            
            
    c.close()

new_url = 'https://search.bilibili.com/all?keyword=嘉然&from_source=nav_suggest_new0&page=1&order=totalrank&duration=0&tids_1=1&tids_2=25'

if __name__ == "__main__":

    # get_video_user_space()
    # spider_util.get_all_video_space()
    # get_video_user_space()
    # get_author_uid()
    get_video_user_space()
    print('all sucess!')
    print('1')
