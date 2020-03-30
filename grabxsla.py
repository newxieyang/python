#! python
# coding=UTF-8
from bs4 import BeautifulSoup
from file_utils import  write_file
from  net_utils  import fetch_source

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
    bs = get_net_content(novel_url)

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
def get_net_content(source_url):
    res = fetch_source(source_url)
    return BeautifulSoup(res, "html.parser")


# 获取文件名
def get_file_name(bs):
    return bs.select(file_name_node)[0].text


# 获取内容
def get_content(catalog_url):
    print(catalog_url)
    bs = get_net_content(catalog_url)
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





if __name__ == '__main__':
    grab_novel()
    # get_content("http://www.cnier.ac.cn/book/1507/827002.html")
