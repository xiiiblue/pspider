#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import datetime
import random
import logging
from logging.config import fileConfig
import mysql.connector
import const

fileConfig('conf/log.conf')


# 导入正式表
def material_import():
    logging.info("开始导入")
    conn = mysql.connector.connect(user=const.DB_USERNAME, password=const.DB_PASSWORD, host=const.DB_HOST,
                                   port=const.DB_PORT, database=const.DB_DATABASE)
    cursor = conn.cursor()

    cursor.execute('select max(id) from publicplatform.material_complex')
    news_oid = cursor.fetchone()[0]  # 生成material_complex表id
    cursor.execute('select max(id),max(sort) from tb_product_recommend')
    values = cursor.fetchone()
    news_recommend_id = values[0]  # 生成tb_product_recommend表id
    news_recommend_sort = values[1]  # 生成tb_product_recommend表sort

    cursor.execute("select * from material_prepare where status='0' order by id")
    values = cursor.fetchall()
    for value in values:
        news_id = value[0]  # 数据取采集表material_prepare主键
        logging.info("导入 " + str(value[1]) + value[3])
        # 插入material_complex表
        news_oid += 1
        group_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + "%03d" % random.randint(0, 999)
        cursor.execute(
            "insert into publicplatform.material_complex (id, account_id, title, author, file_id, summary, add_time, image, "
            + "content, content_url, is_cover, group_id, modity_time, status, type) "
            + "select %s,'113',title,author,null,summary,now(),'',content,'','1',%s,null,null,'0' "
            + "from  material_prepare where id=%s", (news_oid, group_id, news_id))

        # 插入tb_product_recommend表
        news_recommend_id += 1
        news_recommend_sort += 1
        news_recommend_url = 'http://domain.com/path' \
                             + str(news_oid)
        cursor.execute(
            "insert into `tb_product_recommend` (`id`, `appid`, `enter_code`, `sort`, `logourl`, "
            + "`remark`, `webpageurl`, `status`, `name`, `update_time`)"
            + "select %s,%s,'9837000033884704',%s,'0',title,%s,'1',title,now() "
            + "from  material_prepare where id=%s",
            (news_recommend_id, "appid1", news_recommend_sort, news_recommend_url, news_id))
        news_recommend_id += 1
        news_recommend_sort += 1
        cursor.execute(
            "insert into `tb_product_recommend` (`id`, `appid`, `enter_code`, `sort`, `logourl`, "
            + "`remark`, `webpageurl`, `status`, `name`, `update_time`)"
            + "select %s,%s,'9837000033884704',%s,'0',title,%s,'1',title,now() "
            + "from  material_prepare where id=%s",
            (news_recommend_id, "appid2", news_recommend_sort, news_recommend_url, news_id))

        # 更新状态为1，已处理
        cursor.execute("update material_prepare set news_oid=%s,status='1' where id=%s", (news_oid, news_id))
    conn.commit()
    cursor.close()
    logging.info("结束导入")


def test():
    pass
    # material_import()


if __name__ == '__main__':
    test()
