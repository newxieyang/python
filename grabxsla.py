#! python
# coding=UTF-8
from requests import session
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

# 网站url
web_site_url = 'https://www.booktxt.net/'
# 小说url
novel_url = web_site_url + "3_3461/"
# 文件保持路径
file_save_dir = "/Users/cullen/Downloads/"

# 文件名字节点
file_name_node = "#info > h1"
# 目录节点
catalog_node = "#list > dl > dd > a"
# 章节名
title_node = ".bookname > h1"
# 章节内容
content_node = "#content"


def grab_novel():
    bs = fetch_source(novel_url)

    file_name = file_save_dir + get_file_name(bs)

    # 获取目录
    catalog_nodes = bs.select(catalog_node)

    attr_len = len(catalog_nodes)
    print("total of " + str(attr_len) + " chapters")

    # 总页码
    page = 0

    for i in range(31, attr_len):
        if i % 500 == 0:
            page += 1

        catalog_href = novel_url + catalog_nodes[i]['href']
        # print hrf
        content = get_content(catalog_href)
        write_file(file_name + str(page) + ".txt", content)


# 读取网络资源
def fetch_source(source_url):
    headers = {
        'User-Agent': generate_user_agent(device_type='desktop', os=('mac', 'linux', 'win', 'android'))
    }

    s = session()
    resp = s.get(source_url, headers=headers)
    resp.encoding = resp.apparent_encoding
    if resp.status_code == 200:
        return BeautifulSoup(resp.text, "html.parser")
    else:
        fetch_source(source_url)


# 获取文件名
def get_file_name(bs):
    return bs.select(file_name_node)[0].text


# 获取内容
def get_content(catalog_url):
    print(catalog_url)
    bs = fetch_source(catalog_url)
    # print bs
    try:
        title = bs.select(title_node)[0].text
        print(title)
        content_string = bs.select(content_node)[0].text
        return title + "\n" + content_string
    # print str
    except IOError:
        print('IOError')

    return ""


# 写文件
def write_file(file_name, content):
    print(file_name)

    try:
        f = open(file_name, 'a')
        f.write(content)
    finally:
        f.close()


if __name__ == '__main__':
    grab_novel()
    # get_content("http://www.cnier.ac.cn/book/1507/827002.html")
