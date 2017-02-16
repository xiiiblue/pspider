#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from fdfs_client.client import *
import mysql.connector
import logging
from logging.config import fileConfig
import pconvert
import pimport
import const


# 数据采集
def process():
    logging.info("========开始========")
    logging.info("时间: " + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    if sso_login():
        capture_list()
    logging.info("时间: " + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    logging.info("========结束========")


# 模拟登录
def sso_login():
    # 调用单点登录工号认证页面
    response = session.post(const.SSO_URL,
                            data={'login': const.LOGIN_USERNAME, 'password': const.LOGIN_PASSWORD, 'appid': 'np000'})

    # 分析页面，取token及ltpa
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.form.input.get('value')
    ltpa = soup.form.input.input.input.get('value')
    ltpa_value = ltpa.split(';')[0].split('=', 1)[1]

    # 手工设置Cookie
    session.cookies.set('LtpaToken', ltpa_value, domain='unicom.local', path='/')

    # 调用云门户登录页面(2次）
    payload = {'token': token}
    session.post(const.LOGIN_URL, data=payload, proxies=const.PROXIES)
    response = session.post(const.LOGIN_URL, data=payload, proxies=const.PROXIES)
    if response.text == "success":
        logging.info("登录成功")
        return True
    else:
        logging.info("登录失败")
        return False


# 采集列表页面
def capture_list(list_url):
    response = session.get(list_url, proxies=const.PROXIES)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find('div', 'xinwen_list').find_all('a')
    news_list.reverse()
    logging.info("开始采集")
    for news_archor in news_list:
        news_cid = news_archor.attrs['href'].split('=')[1]
        capture_content(news_cid)
    logging.info("结束采集")


# 采集新闻页面
def capture_content(news_cid):
    # 建立DB连接
    conn = mysql.connector.connect(user=const.DB_USERNAME, password=const.DB_PASSWORD, host=const.DB_HOST,
                                   port=const.DB_PORT, database=const.DB_DATABASE)
    cursor = conn.cursor()

    # 判断是否已存在
    cursor.execute('select count(*) from material_prepare where news_cid = %s', (news_cid,))
    news_count = cursor.fetchone()[0]
    if news_count > 0:
        logging.info("采集" + news_cid + ':已存在')
    else:
        logging.info("采集" + news_cid + ':新增')
        news_url = const.NEWS_BASE_URL + news_cid
        response = session.post(news_url, proxies=const.PROXIES)
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, 'html.parser')
        # logging.info(soup)
        news_title = soup.h3.text.strip()[:64]
        news_brief = soup.find('div', 'brief').p.text.strip()[:100]
        news_author = soup.h5.span.a.text.strip()[:100]
        news_content = soup.find('table', 'unis_detail_content').tr.td.prettify()[66:-7].strip()
        # 样式处理
        news_content = pconvert.convert_style(news_content)
        # 将图片转存至DFS并替换URL
        news_content = pconvert.convert_img(news_content)
        # 入表
        cursor.execute(
            'INSERT INTO material_prepare (news_cid, title, author, summary, content, add_time, status)  VALUES  (%s, %s, %s, %s, %s, now(), "0")'
            , [news_cid, news_title, news_author, news_brief, news_content])
    # 提交
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    fileConfig('conf/log.conf')
    session = requests.Session()

    logging.info("========开始========")
    logging.info("时间: " + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    # 采集
    if sso_login():
        # capture_list(const.LIST_URL[0]) #省分新闻
        capture_list(const.LIST_URL[1]) #市分新闻

    # 导入
    # pimport.material_import()

    logging.info("时间: " + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    logging.info("========结束========")
