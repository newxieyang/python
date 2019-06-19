# -*- coding: utf-8 -*-
# author:Apples
import random

from hashlib import md5
from requests import get
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from sqlCommon import *

import time


def request_content(start, end):
    url_link = 'https://datachart.500.com/ssq/history/newinc/history.php?start={0}&end={1}'.format(start, end)
    headers = {
        'User-Agent': generate_user_agent(device_type='desktop', os=('mac', 'linux', 'win', 'android'))
    }
    response = get(url_link, headers=headers, timeout=6)
    page_content = BeautifulSoup(response.content, "html.parser")
    html_tag = page_content.find_all('tbody', id='tdata')[0]
    return html_tag.find_all('tr', 't_tr1')


class ssqclazz:
    def __init__(self):
        self.period = ''  # 期号
        self.red_1 = ''  # 红球
        self.red_2 = ''
        self.red_3 = ''
        self.red_4 = ''
        self.red_5 = ''
        self.red_6 = ''
        self.blue_1 = ''  # 蓝球
        self.lottery_date = ''  # 开奖日期

    def __str__(self):
        return '{0}，{1}，{2}，{3}，{4}，{5}，{6}，{7}，{8}'.format(self.period, self.red_1,
                                                            self.red_2, self.red_3, self.red_4, self.red_5,
                                                            self.red_6, self.blue_1, self.lottery_date)

    def tr_tag(self, tag):
        tds = tag.find_all('td')
        self.period = tds[0].string
        self.red_1 = tds[1].string
        self.red_2 = tds[2].string
        self.red_3 = tds[3].string
        self.red_4 = tds[4].string
        self.red_5 = tds[5].string
        self.red_6 = tds[6].string
        self.blue_1 = tds[7].string
        self.lottery_date = tds[15].string


def ssq_sql(data):
    # 拼接数据
    sql = "insert into ssq (period, red1, red2, red3, red4, red5, red6, blue, lottery_date, md5) VALUES " \
          "({}, {}, {}, {}, {}, {}, {}, {},'{}', '{}')".format(*data)
    # 打印sql
    print(sql)
    mysql_insert(sql)


def trans_data(data):
    # 数据数组
    ssq_data = [data.red_1, data.red_2, data.red_3, data.red_4, data.red_5, data.red_6, data.blue_1, data.lottery_date]
    # 格式化数据
    data_string = '{0}-{1}-{2}-{3}-{4}-{5}-{6}'.format(*ssq_data)
    # md5 加密
    ssq_data.append(md5(data_string.encode("utf-8")).hexdigest())
    # 插入期号
    ssq_data.insert(0, data.period)

    return ssq_data


def grab_ssq():
    # file = open('ssq.txt', mode='a+', encoding='utf-8')
    localtime = time.localtime(time.time())
    lyear = localtime.tm_year
    ymin = 3  # 双色球03年上线
    ymax = lyear - 2000
    print('===抓取数据开始===，200%s-20%s' % (ymin, ymax))
    for year in range(ymin, ymax + 1):
        start = '{0}001'.format(year)
        end = '{0}300'.format(year)
        trs = request_content(start, end)
        for tr in trs:
            ssq_obj = ssqclazz()
            ssq_obj.tr_tag(tr)

            data = trans_data(ssq_obj)
            ssq_sql(data)

            print(tr)
        print()
        time.sleep(3)
    print('抓取完毕！！！')



def check_ssq(md5_string):
    sql = "select count(*) from ssq where md5='{}'".format(md5_string)
    print(sql)
    return mysql_fetchone(sql)

def generate_ssq():
    blue = random.randint(1, 16)

    #
    # s = ''
    # for i in reds:
    #     s += "%02d " % i
    #     # 02d表示是2位数的整数，个数自动补0
    # print(s + "+ " + "%02d" % blue)

    # lists = list(range(1, 34))
    # # 重新排序
    # random.shuffle(lists)
    # red_ball = lists[0:6]
    # red_ball.sort()
    # print(red_ball)

    list2 = list(range(1, 34))
    # 数组里面 随机取样
    red_ball = random.sample(list2, 6)
    red_ball.sort()
    red_ball.append(blue)


    data_string = '{0}-{1}-{2}-{3}-{4}-{5}-{6}'.format(*red_ball)

    md5_string = md5(data_string.encode("utf-8")).hexdigest()

    return_val = check_ssq(md5_string)

    is_exist = int(return_val[0])

    if is_exist > 0:
        generate_ssq()
    else:
        print(red_ball)

    # print(data_string)


if __name__ == '__main__':
    generate_ssq()

    # check_ssq("hhh")
    # grab_ssq()
    # word = ['1', '9', '3', '7']
    # print('{3}-{1}-{2}'.format(*word))
