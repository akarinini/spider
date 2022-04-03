import sqlite3
from fnmatch import fnmatch

from dominate.tags import table
from spider_util import sql_connect


def get_all_data():
    conn = sql_connect()
    all = conn.cursor().execute("SELECT *  from ASOUL_ALL").fetchall()
    conn.close()
    # all:list[(video_url, title, region, view_num, upload_time, up_author, tags, danmu), ...]
    return all

def get_author_name():
    tmp = get_all_data()
    re = []
    for iter in tmp:
        re.append(iter[5])
    return list(set(re))

def get_list_author_name():
    tmp = get_all_data()
    re = []
    for iter in tmp:
        re.append(iter[5])
    return re

def get_died_user():
    conn = sql_connect()
    all = conn.cursor().execute("SELECT *  from ASOUL_ALL where up_author like ?", ('账号注销%',)).fetchall()
    print('有{}个视频的作者投稿过asoul相关的视频却注销了账号'.format(len(all)))
    conn.close()

def get_video_up_2_author():
    list_nums = get_list_author_name()
    set_nums = get_author_name()
    tmp = []
    for i in set_nums:
        if list_nums.count(i) > 1:
            if fnmatch(i, '账号注销*'):
                print('账号注销: {}'.format(i))
                continue
            tmp.append(i)
    print('There is {} authors having > 2 video'.format(len(tmp)))
    return tmp

def get_user_uid():
    conn = sql_connect()
    all = conn.cursor().execute("SELECT *  from AUTHOR_UID").fetchall()
    conn.close()
    re = []
    for iter in all:
        re.append(iter[0])
    return re

if __name__ == "__main__":

    # list_nums = get_list_author_name()
    # set_nums = get_author_name()
    # dicts = {}
    # tmp = []
    # for i in set_nums:
    #     # dicts.update({i : list_nums.count(i)})
    #     if list_nums.count(i) > 1:
    #         tmp.append(i)
    # print(tmp)
    # print(len(tmp))
    conn = sql_connect()
    all = conn.cursor().execute("SELECT *  from ASOUL_ALL where up_author=?", ('贾布加布',)).fetchall()
    print(len(all))
    # conn.close()
    f_name = open("uid.txt", "w+", encoding='UTF-8')
    print('1')