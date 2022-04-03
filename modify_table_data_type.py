import sqlite3

conn = sqlite3.connect('ASOUL.db')
c = conn.cursor()
try:
    c.execute('''DROP TABLE _ASOUL_ALL_API;''')
#    c.execute('''ALTER TABLE ASOUL_ALL_API RENAME TO "_ASOUL_ALL_API";''')
except Exception as e:
    print('sql_connect Error: %s' % e)
try:
    # c.execute('''DROP TABLE _ASOUL_ALL_API;''')
    c.execute('''ALTER TABLE ASOUL_ALL_API RENAME TO "_ASOUL_ALL_API";''')
except Exception as e:
    print('sql_connect Error: %s' % e)
try:
    c.execute('''CREATE TABLE ASOUL_ALL_API
                   (video_url BLOB PRIMARY KEY     NOT NULL UNIQUE,
                   title           BLOB    NOT NULL,
                   region            INTEGER     NOT NULL,
                   view_num        INTEGER     NOT NULL,
                   upload_time       INTEGER   NOT NULL,
                   up_author    BLOB   NOT NULL,
                   tags    BLOB  NOT NULL,
                   danmu    INTEGER   NOT NULL,
                   aid    INTEGER  NOT NULL,
                   comment    INTEGER  NOT NULL,
                   copyright    INTEGER  NOT NULL,
                   length    BLOB  NOT NULL,
                   bvid    BLOB  NOT NULL);''')
    c.execute('''INSERT INTO ASOUL_ALL_API select * from _ASOUL_ALL_API''')
except Exception as e:
    print('sql_connect Error: %s' % e)
    print('no need to create ASOUL_ALL table')
conn.commit()
c.close()