import pymysql
from config import *


def get_db():
    return pymysql.connect(mysql_host, mysql_user, mysql_passwd, "ssq")


## query more
def mysql_fetchall(sql):
    db = get_db()
    cur = db.cursor()
    cur.execute(sql)
    items = cur.fetchall()
    cur.close()
    db.close()

    return items


##query one
def mysql_fetchone(sql):
    # 打开数据库连接
    db = get_db()
    cur = db.cursor()
    cur.execute(sql)
    item = cur.fetchone()
    cur.close()
    db.close()

    return item


## insert
def mysql_insert(sql):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    cur.close()
    db.close()


## delete
def mysql_delete(sql):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    cur.close()
    db.close()


## update
def mysql_update(sql):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

    cur.close()
    db.close()


## test sql
def main():
    data = [1, 2, 3, 4, 5, 6, 7, 8, "2019-08-03", '00000']
    sql = "insert into ssq (period, red1, red2, red3, red4, red5, red6, blue, lottery_date, md5) VALUES " \
          "({}, {}, {}, {}, {}, {}, {}, {},'{}', '{}')".format(*data)
    # "('%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d','%s')" % \
    # (1, 2, 3, 4, 5, 6, 7, 8, "2019-08-03")

    print(sql)
    mysql_insert(sql)
    item = mysql_fetchone("select * from ssq limit 1")
    print(item)


## test
if __name__ == '__main__':
    main()
