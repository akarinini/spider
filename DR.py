from asoul import AllTag, AllTag2
from spider_util import get_space_video_by_api
import sqlite3
import time
import random
import logging
import datetime

dir = "/home/ubuntu/AsoulLog/DR/"

fname = dir + "dr" + datetime.datetime.now().strftime("%Y%m%d") + ".log"

logging.basicConfig(level=logging.DEBUG #设置日志输出格式
                    ,filename=fname #log日志输出的文件位置和文件名
                    # ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                    )

search_api = 'https://api.bilibili.com/x/web-interface/search/type?context=&search_type=video&page={}&order=pubdate&keyword={}&duration=0&category_id=&tids_2=&__refresh__=true&_extra=&tids=0&highlight=1&single_column=0'

if __name__ == "__main__":
    c = sqlite3.connect('ASOUL.db')
    # start_spider(AllTag, order, duration, tid)
    for itag in AllTag:
        # print('itag : {}'.format(itag))
        time.sleep(random.random() / 10 + 0.2)
        a = get_space_video_by_api(search_api.format(1, itag))
        numPages = (a['data']['numPages'])
        numPages = 10 # 先给10页
        # print('numPages : {}'.format(numPages))
        for ipage in range(1, numPages):
            time.sleep(random.random() / 10 + 0.2)
            # print('ipage : {}'.format(ipage))
            # print('search_url : {}'.format(search_api.format(ipage, itag)))
            a = get_space_video_by_api(search_api.format(ipage, itag))
            result = a['data']['result']
            for item in result:
                bvid = str(item['bvid'])
                title = str(item['title'])
                view_num = str(item['play'])
                region = str(item['typeid']) # 分区
                danmu = str(item['video_review']) 
                up_author = str(item['author'])
                up_author_uid = str(item['mid'])
                upload_time = str(item['senddate'])
                aid = str(item['aid'])
                comment = str(item['review'])
                # copyright = str(item['copyright']) # 自制或转载
                length = str(item['duration'])
                store = str(item['favorites']) # 收藏
                like = str(item['like']) # 点赞
                str_tag = str(item['tag'])
                video_url = 'https://www.bilibili.com/video/{}?from=search'.format(bvid)

                if set(str_tag.split(',')) & set(AllTag2):
                    c.execute("INSERT OR IGNORE INTO ASOUL_ALL_API VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (str(video_url), str(title), int(region), int(view_num), int(upload_time),
                                        str(up_author), str(str_tag), int(danmu), int(aid), int(comment), 1, length, bvid))
                    c.execute("INSERT OR IGNORE INTO AUTHOR_UID VALUES (?, ?)",
                          (str(up_author_uid), str(up_author)))
                    logging.info("title:{} tag:{} video_url:{}".format(title, str_tag, video_url))
                    c.commit()
                
        # print(item)
    c.close()
    # print(a)

