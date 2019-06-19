#!/usr/bin/python3
# coding=UTF-8
from requests import session
from bs4 import BeautifulSoup

web_site_url = 'http://bibizyz5.com/'

# 文件保持路径
file_save_dir = "/Users/cullen/Downloads/images"


# 读取网络资源
def fetch_source(source_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}

    s = session()
    r = s.get(source_url, headers=headers)
    if r.status_code == 200:
        return BeautifulSoup(r.text, "html.parser")
    else:
        fetch_source(source_url)


def grab_novel():
    bs = fetch_source(web_site_url)

    # file_name = file_save_dir + get_file_name(bs)

    # 获取目录
    catalog_nodes = bs.select("table")

    attr_len = len(catalog_nodes)
    print("total of " + str(attr_len) + " chapters")

    # 总页码
    page = 0

    for i in range(1865, attr_len):
        if i % 500 == 0:
            page += 1

        catalog_href = web_site_url + catalog_nodes[i]['href']
        # # print hrf
        # content = get_content(catalog_href)
        # write_file(file_name + str(page) + ".txt", content)
