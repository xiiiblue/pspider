#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from fdfs_client.client import *
import const

# 初始化dfs客户端
dfs_client = Fdfs_client('conf/dfs.conf')


# 文本样式处理
def convert_style(rawtext):
    newtext = '<div style="margin-left: 0px; margin-right:0px; letter-spacing: 1px; word-spacing:2px;line-height: 1.7em; font-size:18px;text-align:justify; text-justify:inter-ideograph">' \
              + rawtext + '</div>'
    newtext = newtext.replace(' align="center"', '')
    soup = BeautifulSoup(newtext, 'html.parser')
    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        del img_tag.parent['style']
    return soup.prettify()


# 文本中图片替换
def convert_img(rawtext):
    soup = BeautifulSoup(rawtext, 'html.parser')
    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        raw_img_url = img_tag['src']
        dfs_img_url = convert_url(raw_img_url)
        img_tag['src'] = dfs_img_url
        del img_tag['style']
    return soup.prettify()


# 图片转存至DFS
def convert_url(raw_img_url):
    response = requests.get(raw_img_url, proxies=const.PROXIES)
    pic_buffer = response.content
    pic_ext = raw_img_url.split('.')[-1]
    response = dfs_client.upload_by_buffer(pic_buffer, pic_ext)
    dfs_img_url = const.DFS_BASE_URL + '/' + response['Remote file_id']
    return dfs_img_url


def test():
    pass

if __name__ == '__main__':
    test()
