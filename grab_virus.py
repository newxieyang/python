#! python
# coding=UTF-8
from net_utils import *
import prettytable as pt
import json

# 奥匈解体后分裂成10个小国， 要分开计算
url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
major_members = ['美国', '意大利', "德国",'法国','英国','日本本土', '俄罗斯']
o_members = ['奥地利','匈牙利','捷克','斯洛伐克','塞尔维亚','黑山','克罗地亚','斯洛文尼亚','北马其顿','波黑']
population = {'美国':33000, '意大利':6043, "德国":8292,'法国':6698,'英国':6648,'日本本土':12477, '俄罗斯':14447, '奥匈':5440}

# 获取列表的第二个元素
def take_second(elem):
    return elem[2]


def top_ten_data(items):

    tb2 = pt.PrettyTable()
    tb2.field_names = ["国家", "确诊", "死亡", "死亡率"]

    sum_dead = 0
    sum_confirm = 0

    for item in items[:10]:
        dead_rate = '{:.2%}'.format(item['dead']/item['confirm'])
        tb2.add_row([item['name'], item['confirm'], item['dead'], dead_rate])
        sum_dead +=  item['dead']
        sum_confirm += item['confirm']

    dead_rate = '{:.2%}'.format(sum_dead/sum_confirm)
    tb2.add_row(['合计', sum_confirm,  sum_dead, dead_rate])
    print(tb2)

def major_members_data(items):

    members = major_members + o_members

    index = 0
    tb = pt.PrettyTable()
    tb.field_names = ["国家", "确诊", "死亡", "死亡率"]
    sum_dead  = 0
    sum_confirm = 0

    for item in items:
        if index < 17:
            if item['name'] in members:
                sum_dead +=  item['dead']
                sum_confirm += item['confirm']
                dead_rate = '{:.2%}'.format(item['dead']/item['confirm'])
                tb.add_row([item['name'], item['confirm'], item['dead'], dead_rate])
                index += 1
        if index == 17:
            break

    dead_rate = '{:.2%}'.format(sum_dead/sum_confirm)
    tb.add_row(['合计', sum_confirm, sum_dead, dead_rate])
    print(tb)

def allies(items):
    sum_dead = 0
    sum_confirm = 0

    # 奥匈帝国
    o_sum_dead = 0
    o_sum_confirm = 0

    tb = pt.PrettyTable()
    tb.field_names = ["国家", '人口', "确诊", '确诊率',"死亡", "死亡率"]

    list =[]

    count1 = 0 #联军总数（剔除奥匈）
    count2 = 0  #奥匈帝国解体后的国家总数
    # 总共有170多个国家， 把联军分开，累计，联军国家遍历后就退出循环
    for item in  items:
        if count1 < 7:
            if item['name'] in major_members:
                count1 +=1
                sum_confirm += item['confirm']
                sum_dead += item['dead']
                confirm_rate = '{:.4%}'.format(item['confirm']/(population[item['name']]*10000))
                dead_rate = '{:.2%}'.format(item['dead']/item['confirm'])
                list.append([item['name'], population[item['name']], item['confirm'], confirm_rate, item['dead'], dead_rate])
        if count2 < 10:
            if item['name'] in o_members:
                count2 +=  1
                o_sum_confirm += item['confirm']
                o_sum_dead += item['dead']
        if count1 == 7 and count2 == 10:
            break


    dead_rate = '{:.2%}'.format(o_sum_dead/o_sum_confirm)
    confirm_rate = '{:.4%}'.format(o_sum_confirm/(population['奥匈']*10000))
    list.append(["奥匈", population['奥匈'], o_sum_confirm, confirm_rate, o_sum_dead, dead_rate])

    list.sort(key=take_second, reverse=True)

    for item in list:
        tb.add_row(item)


    sum_confirm += o_sum_confirm
    sum_dead += o_sum_dead

    total_dead_rate = '{:.2%}'.format(sum_dead/sum_confirm)
    total_confirm_rate = '{:.2%}'.format(sum_confirm/930450000)
    tb.add_row(["合计",93045, sum_confirm, total_confirm_rate, sum_dead, total_dead_rate])
    print("人口单位是万， 死亡率是基于确诊人数")
    print(tb)

if __name__ == '__main__':

    res = fetch_source(url)
    data_dic = json.loads(res)
    items = data_dic['data']
    if items is not None:
        major_members_data(items)
        top_ten_data(items)
        allies(items)

