from http.client import HTTPException
from flask import Flask, request
import sqlite3
import json
from waitress import serve
import logging
import os
import datetime
app = Flask(__name__)

@app.before_first_request
def before_first_request():
    log_level = logging.INFO

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'ApiLogs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    
    fname = "api" + datetime.datetime.now().strftime("%Y%m%d") + ".log"
    log_file = os.path.join(logdir, fname)
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    app.logger.setLevel(log_level)

@app.route("/AsoulRT-top30")
def welcome():
    c = sqlite3.connect('ASOUL_RANK.db')
    all = c.cursor().execute("SELECT *  from DR_RANK ORDER BY timeStamp DESC").fetchone()
    c.close()
    dict = json.loads(all[1])
    dict["timeStamp"] = all[0]
    result = json.dumps(dict, ensure_ascii=False)
    return result

@app.route("/AsoulRT-FanArt")
def FanArt():
    page = int(request.args.get("page"))
    if (page != 1):
        return json.dumps({"code": 404, "message": "not found", "ttl": 1, "data": {"page": page, "numResults": 0, "result":[]}}, ensure_ascii=False)
    else:
        c = sqlite3.connect('ASOUL_RANK.db')
        all = c.cursor().execute("SELECT *  from DR_RANK_YUAN_CHUANG ORDER BY timeStamp DESC").fetchone()
        c.close()
        dict = json.loads(all[1])
        # dict["timeStamp"] = all[0]
        result = json.dumps(dict, ensure_ascii=False)
        return result

@app.route("/AsoulRT-Cut")
def Cut():
    page = int(request.args.get("page"))
    if (page != 1):
        return json.dumps({"code": 404, "message": "not found", "ttl": 1, "data": {"page": page, "numResults": 0, "result":[]}}, ensure_ascii=False)
    else:
        c = sqlite3.connect('ASOUL_RANK.db')
        all = c.cursor().execute("SELECT *  from DR_RANK_ZHUAN_ZAI ORDER BY timeStamp DESC").fetchone()
        c.close()
        dict = json.loads(all[1])
        # dict["timeStamp"] = all[0]
        result = json.dumps(dict, ensure_ascii=False)
        return result

@app.route("/AsoulPudateVedio")
def pudate_vedio():
    page = int(request.args.get("page"))
    pagesize = 20
    c = sqlite3.connect('ASOUL.db')
    all = c.cursor().execute("SELECT bvid from ASOUL_ALL_API ORDER BY upload_time DESC  LIMIT ? OFFSET ?",(pagesize, (page-1)*pagesize,)).fetchall()
    transfer_json = {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "page": page,
            "numResults": pagesize,
            "result": all
        }
    }
    app.logger.info(str(datetime.datetime.now()) + "  " + str(request.remote_addr))
    result = json.dumps(transfer_json, ensure_ascii=False)
    return result

@app.route("/AsoulMostViewVedio")
def most_view_vedio():
    page = int(request.args.get("page"))
    pagesize = 20
    c = sqlite3.connect('ASOUL.db')
    all = c.cursor().execute("SELECT bvid from ASOUL_ALL_API ORDER BY view_num DESC  LIMIT ? OFFSET ?",(pagesize, (page-1)*pagesize,)).fetchall()
    transfer_json = {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "page": page,
            "numResults": pagesize,
            "result": all
        }
    }
    app.logger.info(str(datetime.datetime.now()) + "  " + str(request.remote_addr))
    result = json.dumps(transfer_json, ensure_ascii=False)
    return result

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5200, debug=True)
    serve(app, host="0.0.0.0", port=5200, threads=6) # 运行
    # app.run(host="127.0.0.1", port=5200, debug=True) # 单机测试
