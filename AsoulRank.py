import sqlite3
from filecmp import cmp
from sqlite3.dbapi2 import Timestamp
from spider_util import sql_connect
from spider_util import get_space_video_by_api
import time
import json
import logging
import datetime

dir = "/home/ubuntu/AsoulLog/AsoulRank/"

fname = dir + "Rank" + datetime.datetime.now().strftime("%Y%m%d") + ".log"

logging.basicConfig(level=logging.DEBUG #设置日志输出格式
                    ,filename=fname #log日志输出的文件位置和文件名
                    # ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                    )

video_data_api = 'https://api.bilibili.com/x/web-interface/view?bvid={}'

def cal_score(view, danmaku, reply, favorite, coin, share, like, dislike):
    return int(view)*0.25 + (int(danmaku)+int(coin)+int(reply)+int(like)-int(dislike))*0.4 + int(favorite)*0.3 + int(share)*0.6


def sql_connect_rank():
    conn = sqlite3.connect('ASOUL_RANK.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE DR_RANK
                   (timeStamp INT PRIMARY KEY     NOT NULL UNIQUE,
                   rankJson           BLOB    );''')
        c.execute('''CREATE TABLE DR_RANK_YUAN_CHUANG
                   (timeStamp INT PRIMARY KEY     NOT NULL UNIQUE,
                   rankJson           BLOB    );''')
        c.execute('''CREATE TABLE DR_RANK_ZHUAN_ZAI
                   (timeStamp INT PRIMARY KEY     NOT NULL UNIQUE,
                   rankJson           BLOB    );''')
    except Exception as e:
        print('sql_connect Error: %s' % e)
        print('no need to create DR_RANK table')
    return conn

def timestamp_convert_localdate(timestamp,time_format="%Y/%m/%d %H:%M:%S"):
    # 按照当前设备时区来进行转换，比如当前北京时间UTC+8
    timeArray = time.localtime(timestamp)
    styleTime = time.strftime(str(time_format), timeArray)
    return styleTime 


if __name__ == "__main__":

    conn = sqlite3.connect('ASOUL.db')
    all = conn.cursor().execute("SELECT * from ASOUL_ALL_API").fetchall()
    conn.close()

    bvid = []
    local_timestamp = int(time.time())
    for i in all:
        if int(i[4]) >= (local_timestamp - 3*24*60*60):
            bvid.append(i)

    AllRank = []
    transfer_json = {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "numResults": 30,
            "result": []
        }
    }
    for i in bvid:
        # print('bvid={}'.format(i[12]))
        time.sleep(0.1)
        video_json = get_space_video_by_api(video_data_api.format(i[12]))
        if video_json == 62002:
            continue
        elif video_json == -404:
            continue
        else:
            data = video_json['data']['stat']
            score = cal_score(danmaku=data['danmaku'], view=data['view'], reply=data['reply'], favorite=data['favorite'], coin=data['coin'], share=data['share'], like=data['like'], dislike=data['dislike'])
            AllRank.append([i[12], int(score)])

    AllRank.sort(key=lambda x: x[1])

    zhuan_zai_list = []
    yuan_chuang_list = []

    AllRank = list(reversed(AllRank))
    for i in AllRank[:30]:
        time.sleep(0.1)
        video_json = get_space_video_by_api(video_data_api.format(i[0]))
        copyright = video_json['data']['copyright']
        if (len(zhuan_zai_list) <= 60) & (int(copyright) == 2):
            zhuan_zai_list.append([video_json['data']['bvid'],])
        if (len(yuan_chuang_list) <= 60) & (int(copyright) == 1) & (video_json['data']['owner']['mid'] != 672328094) & (video_json['data']['owner']['mid'] != 351609538) & (video_json['data']['owner']['mid'] != 672346917) & (video_json['data']['owner']['mid'] != 672342685) & (video_json['data']['owner']['mid'] != 672353429):
            yuan_chuang_list.append([video_json['data']['bvid'],])
        video_json['data']['score'] = int(i[1])
        transfer_json['data']['result'].append(video_json['data'])
    
    for i in AllRank[30:]:
        if len(zhuan_zai_list) == 60 & len(yuan_chuang_list) == 60:
            break
        time.sleep(0.1)
        video_json = get_space_video_by_api(video_data_api.format(i[0]))
        copyright = video_json['data']['copyright']
        if (len(zhuan_zai_list) <= 60) & (int(copyright) == 2):
            zhuan_zai_list.append([video_json['data']['bvid'],])
        if (len(yuan_chuang_list) <= 60) & (int(copyright) == 1) & (video_json['data']['owner']['mid'] != 672328094) & (video_json['data']['owner']['mid'] != 351609538) & (video_json['data']['owner']['mid'] != 672346917) & (video_json['data']['owner']['mid'] != 672342685) & (video_json['data']['owner']['mid'] != 672353429):
            yuan_chuang_list.append([video_json['data']['bvid'],])


    zhuan_zai_transfer_json = {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "page": 1,
            "numResults": 60,
            "result": zhuan_zai_list
        }
    }
    yuan_chuang_transfer_json = {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "page": 1,
            "numResults": 60,
            "result": yuan_chuang_list
        }
    }

    storage_json = json.dumps(transfer_json, ensure_ascii=False)
    zhuan_zai_transfer_json = json.dumps(zhuan_zai_transfer_json, ensure_ascii=False)
    yuan_chuang_transfer_json = json.dumps(yuan_chuang_transfer_json, ensure_ascii=False)


    # print(storage_json)
    logging.info(storage_json)

    conn = sqlite3.connect('ASOUL_RANK.db')
    conn.execute("INSERT OR IGNORE INTO DR_RANK VALUES (?, ?)",
              (local_timestamp, str(storage_json)))
    conn.execute("INSERT OR IGNORE INTO DR_RANK_YUAN_CHUANG VALUES (?, ?)",
              (local_timestamp, str(yuan_chuang_transfer_json)))
    conn.execute("INSERT OR IGNORE INTO DR_RANK_ZHUAN_ZAI VALUES (?, ?)",
              (local_timestamp, str(zhuan_zai_transfer_json)))
    conn.commit()
    conn.close()

    # print('end')
