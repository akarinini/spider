from spider_util import get_space_video_by_api
import sqlite3
import time
import random
import logging
import datetime

dir = "/home/ubuntu/AsoulLog/DR/"

fname = dir + "dr" + datetime.datetime.now().strftime("%Y%m%d") + ".log"

AllTag = ['嘉然', '向晚', '贝拉', '珈乐', '乃琳', 'asoul']

logging.basicConfig(level=logging.DEBUG #设置日志输出格式
                    ,filename=fname #log日志输出的文件位置和文件名
                    # ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                    )

search_api = 'https://api.bilibili.com/x/web-interface/search/type?context=&search_type=video&page={}&order=pubdate&keyword={}&duration=0&category_id=&tids_2=&__refresh__=true&_extra=&tids=0&highlight=1&single_column=0'
video_data_api = 'https://api.bilibili.com/x/web-interface/view?bvid={}'

if __name__ == "__main__":
    c = sqlite3.connect('ASOUL.db')
    # start_spider(AllTag, order, duration, tid)
    for itag in AllTag:
        # print('itag : {}'.format(itag))
        time.sleep(random.random() / 10 + 0.2)
        a = get_space_video_by_api(search_api.format(1, itag))
        # numPages = (a['data']['numPages'])
        numPages = 10 # 前10页
        # print('numPages : {}'.format(numPages))
        for ipage in range(1, numPages):
            time.sleep(random.random() / 10 + 0.2)
            # print('ipage : {}'.format(ipage))
            # print('search_url : {}'.format(search_api.format(ipage, itag)))
            a = get_space_video_by_api(search_api.format(ipage, itag))
            result = a['data']['result']
            for item in result:
                bvid = str(item['bvid'])
                videoData = get_space_video_by_api(video_data_api.format(bvid))
                if videoData['code'] == 0:
                    name = videoData['data']['owner']['name']
                    mid = videoData['data']['owner']['mid']
                    face = videoData['data']['owner']['face']
                    tid = videoData['data']['tid']
                    tname = videoData['data']['tname']
                    copyright = videoData['data']['copyright']
                    aid = videoData['data']['aid']
                    title = videoData['data']['title']
                    pic = videoData['data']['pic']
                    tag = item['tag']
                    pubdate = videoData['data']['pubdate']
                    duration = videoData['data']['duration']
                    view = videoData['data']['stat']['view']
                    danmaku = videoData['data']['stat']['danmaku']
                    reply = videoData['data']['stat']['reply']
                    favorite = videoData['data']['stat']['favorite']
                    coin = videoData['data']['stat']['coin']
                    share = videoData['data']['stat']['share']
                    like = videoData['data']['stat']['like']
                    score = int(view * 0.25 + (like + coin + reply + like) * 0.4 + favorite * 0.3 + share * 0.6)
                    logging.info("title:{} tag:{} bvid:{}".format(title, tag, bvid))
                # 插入数据库
                
                else:
                    print(videoData)
                # if set(str_tag.split(',')) & set(AllTag2):
                #     c.execute("INSERT OR IGNORE INTO ASOUL_ALL_API VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                #                         (str(video_url), str(title), int(region), int(view_num), int(upload_time),
                #                         str(up_author), str(str_tag), int(danmu), int(aid), int(comment), 1, length, bvid))
                #     c.execute("INSERT OR IGNORE INTO AUTHOR_UID VALUES (?, ?)",
                #           (str(up_author_uid), str(up_author)))
                #     logging.info("title:{} tag:{} video_url:{}".format(title, str_tag, video_url))
                #     c.commit()
                
        # print(item)
    c.close()
    # print(a)

