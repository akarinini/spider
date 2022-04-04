from spider_util import get_space_video_by_api
import sqlite3

conn = sqlite3.connect('ASOUL.db')
all = conn.cursor().execute("SELECT bvid,tags from ASOUL_ALL_API").fetchall()
conn.close()

video_data_api = 'https://api.bilibili.com/x/web-interface/view?bvid={}'

for video in all:
    bvid = video[0]
    tag = video[1]
    # 有些tag
    if tag.startswith('[') & tag.endswith(']'):
        tag = tag[2:-2]
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
        # 插入数据库

    else:
        print(videoData)