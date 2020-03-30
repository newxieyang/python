#! python
# coding=UTF-8
from net_utils import *
import prettytable as pt
import json

qq_url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?country='
select_country = ['美国', '意大利', "德国",'法国','英国','日本本土', '俄罗斯']
split_country = ['奥地利','匈牙利','捷克','斯洛伐克','塞尔维亚','黑山','克罗地亚','斯洛文尼亚','北马其顿','波黑']

# # 读取网络资源
# def fetch_source(url):
#     headers = {
#         'User-Agent': generate_user_agent(device_type='desktop', os=('mac', 'linux', 'win', 'android'))
#     }
#
#     s = session()
#     resp = s.get(url, headers=headers)
#     resp.encoding = resp.apparent_encoding
#     if resp.status_code == 200:
#        return parse_data(resp.text)
#     else:
#         fetch_source(url)


def parse_data(data):
    data_dic = json.loads(data)
    items = data_dic['data']
    if items is not None:
        return items[-1]

# 获取列表的第二个元素
def take_second(elem):
    return elem[1]


if __name__ == '__main__':

    sum_dead = 0
    sum_confirm = 0
    sum_add = 0
    tb = pt.PrettyTable()
    tb.field_names = ["国家", "确诊","新增", "死亡", "死亡率"]

    list =[]

    # 七国
    for item in select_country:
        res = fetch_source(qq_url + item)
        result = parse_data(res)
        sum_confirm += result['confirm']
        sum_dead += result['dead']
        sum_add += result['confirm_add']
        percent = '{:.2%}'.format((result['dead']/result['confirm']))
        list.append([item, result['confirm'], result['confirm_add'], result['dead'], percent])

    # 奥匈帝国
    count_split_dead = 0
    count_split_confirm = 0
    count_split_add = 0
    for item in split_country:
        res = fetch_source(qq_url + item)
        result = parse_data(res)
        count_split_confirm += result['confirm']
        count_split_dead += result['dead']
        count_split_add += result['confirm_add']

    percent = '{:.2%}'.format(count_split_dead/count_split_confirm)
    list.append(["奥匈", count_split_confirm, count_split_add, count_split_dead, percent])

    list.sort(key=take_second, reverse=True)

    for item in list:
        tb.add_row(item)


    sum_confirm += count_split_confirm
    sum_dead += count_split_dead
    sum_add +=  count_split_add

    total_percent = '{:.2%}'.format(sum_dead/sum_confirm)
    tb.add_row(["合计", sum_confirm, sum_add, sum_dead, total_percent])
    print(tb)

