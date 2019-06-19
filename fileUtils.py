#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 读取文件
def read(filename):
    try:
        f = open(filename, 'r')
        print(f.read())
    finally:
        if f:
            f.close()


# 按行读取文件
def read_lines(filename):
    print(filename)
    try:
        f = open(filename, 'r')
        for line in f.readlines():
            print(line.strip())
    finally:
        if f:
            f.close()


# 写文件
def write_file(filename, content):
    print(filename)
    try:
        f = open(filename, 'a')
        f.write(content)
    finally:
        if f:
            f.close()

            # writeFile('/Users/cullen/Downloads/README2.txt','hello...cullen')
