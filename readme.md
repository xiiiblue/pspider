# pspyder新闻爬虫

## 应用简介
pspyder新闻爬虫，是一个新闻采集类应用，能够自动模拟登录并采集网站上的新闻内容，将新闻加工后，同步到生产库。

## 功能特性
- 通过伪造cookie，模拟单点登录认证
- 新闻列表、新闻正文内页面采集
- 支持代理服务器
- HTML文本CSS样式调整，适配手机屏幕
- HTML文本中图片转存并替换URL
- 支持上传至FastDFS分布式文件系统
- 采集结果导入生产库
- 日志打印

## 第三方依赖
- [requests](http://www.python-requests.org/en/master) - 更为人性化的网络连接库
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup) - HTML数据的解析库
- [fdfs_client-py](https://github.com/hay86/fdfs_client-py) - FastDFS客户端

## 依赖安装
大部分依赖直接使用pip3安装即可
```
sudo apt-get install python3-pip
sudo pip3 install requests
sudo pip3 install beautifulsoup4
sudo pip3 install mysql-connector
```
注意：
fdfs_client-py不能直接使用pip3安装，需要直接使用一个python3版的源码，并手工修改其中代码。操作过程如下：
```
git clone https://github.com/jefforeilly/fdfs_client-py.git
cd dfs_client-py
vi ./fdfs_client/storage_client.py
将第12行 from fdfs_client.sendfile import * 注释掉
python3 setup.py install

sudo pip3 install mutagen
```

## 建表语句
```
CREATE TABLE `material_prepare` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `news_cid` varchar(64) NOT NULL COMMENT '云门户新闻ID',
  `news_oid` varchar(64) DEFAULT NULL COMMENT '掌沃行中新闻ID',
  `title` varchar(64) NOT NULL DEFAULT '' COMMENT '标题',
  `author` varchar(100) NOT NULL COMMENT '作者',
  `summary` varchar(120) DEFAULT NULL COMMENT '摘要',
  `content` text NOT NULL COMMENT '内容',
  `add_time` timestamp NULL DEFAULT NULL COMMENT '新增时间',
  `status` varchar(1) DEFAULT NULL COMMENT '状态 0：草稿 1：正文',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;
```

## crontab配置
```
crontab -e
0 16 * * *    /home/pyapp/pspider/pspider.py
```

## CentOS下Python3环境配置

### 设置代理
```
export http_proxy="http://xxx.xxx.xxx.xxx:31081"
```

### 源码方式安装python3
```
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
tar -zxcf Python-3.6.0.tgz
./configure
make && make install
```

### 使pip走代理
```
alias pip3="pip3 --proxy xxx.xxx.xxx.xxx:31081"
```
