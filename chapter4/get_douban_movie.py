#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

def get_allmovie(tags):
    # 定义一个列表存储电影的基本信息
    movies = []
    # 处理每个tag
    for tag in tags:
        start = 0
        # 不断请求，直到返回结果为空
        while 1:
            # 拼接需要请求的链接，包括标签和开始编号
            url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + tag + '&sort=recommend&page_limit=20&page_start=' + str(start)
            print(url)
            res = requests.get(url)
            res.encoding = 'utf-8'
            # 加载json为字典
            res = res.json()

            # 先在浏览器中访问一下API，观察返回json的结构
            # 然后在Python中取出需要的值
            result = res['subjects']

            # 返回结果为空，说明已经没有数据了
            # 完成一个标签的处理，退出循环
            if len(result) == 0:
                break

            # 将每一条数据都加入movies
            for item in result:
                movies.append(item)

            # 使用循环记得修改条件
            # 这里需要修改start
            start += 20

    # 看看一共获取了多少电影
    print(len(movies))
    get_detail(movies)
    store_txt(movies)

def get_detail(movies):
    # 请求每部电影的详情页面
    for x in range(0, len(movie)):
        url = movies[x]['url']
        res = requests.get(url)
        res.encoding = 'utf-8'
        # 使用BeautifulSoup解析html
        html = BeautifulSoup(res.text,'html.parser')
        # 提取电影简介
        # 捕捉异常，有的电影详情页中并没有简介
        try:
            description = html.find_all("span", attrs={"property": "v:summary"})[0].get_text()
        except Exception as e:
            # 没有提取到简介，则简介为空
            movies[x]['description'] = ''
        else:
            # 将新获取的字段填入movies
            movies[x]['description'] = description
            print(description)
        finally:
            pass

        # 适当休息，避免请求频发被禁止，报403 Forbidden错误
        time.sleep(0.5)
def store_txt(movies):
    fw = open('douban_movies.txt', 'w',encoding='utf-8')
    # 写入一行表头，用于说明每个字段的意义
    fw.write('title^rate^url^cover^id^description\n')
    for item in movies:
        # 用^作为分隔符
        # 主要是为了避免中文里可能包含逗号发生冲突
        fw.write(item['title'] + '^' + item['rate'] + '^' + item['url'] + '^' + item['cover'] + '^' + item['id'] + '^' + item['description'] + '\n')
    fw.close()

if __name__== "__main__":
    # 获取所有标签
    tags = []
    url = 'https://movie.douban.com/j/search_tags?type=movie'
    res = requests.get(url)
    res.encoding = 'utf-8'
    # 加载json为字典
    res = res.json()
    tags = res['tags']
    get_allmovie(tags)