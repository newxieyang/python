#! python
# coding=UTF-8
from requests import session
from bs4 import BeautifulSoup
import sys
import writeFile

reload(sys)

# sysCharType = sys.getfilesystemencoding()
sys.setdefaultencoding('UTF-8')

# 网站url
web_site_url = 'http://www.xs.la'
# 小说url
novel_url = web_site_url + "/1_1677"
# 文件保持路径
file_save_dir= "/Users/xieyang/Downloads/"

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
	print ("total of " + bytes(attr_len) + " chapters")

	# 总页码
	page = 0

	for i in range(1865,attr_len):
		if i%500 == 0:
			page += 1

		catalog_href = web_site_url + catalog_nodes[i]['href']
		# print hrf
		content = get_content(catalog_href)
		write_file(file_name + str(page) + ".txt", content)




# 读取网络资源
def fetch_source(source_url):
	headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}

	s = session()
	r = s.get(source_url, headers=headers)
	if r.status_code == 200:
		return BeautifulSoup(r.text, "html.parser")
	else:
		fetch_source(source_url)


# 获取文件名
def get_file_name(bs):
	return bs.select(file_name_node)[0].text


# 获取内容
def get_content(catalog_url):

	print (catalog_url)
	bs = fetch_source(catalog_url)
	# print bs
	try:
		title = bs.select(title_node)[0].text
		print (title)
		content_string = bs.select(content_node)[0].text
		return title + "\n" + content_string
		# print str
	except IOError, e:
		print 'IOError', e

	return ""


# 写文件
def write_file(file_name, content):
	print file_name

	try:
		f = open(file_name, 'a')
		f.write(content)
	finally:
		f.close()

grab_novel()
# get_content("http://www.cnier.ac.cn/book/1507/827002.html")
