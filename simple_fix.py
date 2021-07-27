
# simple fix
from flask import Flask, jsonify, render_template, request, url_for, redirect, make_response
from AES import decrypt
import sys
import base64
import os
from shutil import copy
import json
import pymysql
import io

# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)

key = '123456_Encrypting'
@app.route('/')
def index():
    # print(sys.argv[0])
    return render_template('index.html')

def get_connection():
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='image_search_db', charset='utf8')
    return connection

# @app.route('/images/<keyword>')
def get_img(keyword):
    # 匹配用户输入keyword的语句
    connection = get_connection()
    cur = connection.cursor()

    try:
        # 两种修复方式：
        # 一种直接不返回
        # 一种sql语句级修复
        sql = "SELECT * FROM image_info WHERE image_name like '%" + keyword + "%'"

        cur.execute(sql)
    except Exception as e:
        pass
        # return e

    data = cur.fetchall()
    # print(data)
    # print('-'*100)

    decrypted_data_dicts = []

    for info in data:
        info_dict = {}
        info_dict['image_name'] = info[0]
        info_dict['image_path'] = decrypt(key, info[1])
        decrypted_data_dicts.append(info_dict)

    # print(type({"image_list": decrypted_data_dicts}))
    return {"image_list": decrypted_data_dicts}


result_folder = 'static/search_results/'

@app.route('/image/<image_name>', methods=['POST'])
def img_to_byte_stream(image_name):
    with open('static/search_results/' + image_name, 'rb') as fp:
        bs = fp.read()

    # print(bs)
    # construct http response include byte stream

    response = make_response(bs)

    response.headers.set('Content-Type', 'image/jpeg')
    # print('response: {}'.format(response))
    return response


@app.route('/search')
def search():
    # 获取GET数据
    keyword = request.args.get('keyword')
    # print('keyword: {}'.format(keyword))

    result = get_img(keyword)
    # print('result: {}'.format(result))

    if type(result) is dict:
        # print(result)
        # json = {
#     'image_list': [
#         {
#     "image_name" : "cat_img_000000.jpg",
#     "image_path" : "img/cat_img/cat_img_000000.jpg"
#     },
#         {"image_name" : "cat_img_000001.jpg",
#     "image_path" : "img/cat_img/cat_img_000002.jpg"}
#     ]
# }
        result_num = len(result["image_list"])

        show_img_paths = []
        image_names = []
        # image_streams = []

        for i in range(result_num):
            img_path = result['image_list'][i]["image_path"]
            image_name = result['image_list'][i]["image_name"]

            # image_streams.append(img_to_byte_stream(img_path))

            show_img_path = result_folder + image_name
            # show_img_paths.append(show_img_path)
            image_names.append(image_name)

            try:
                copy(img_path, show_img_path)
            except:
                pass


        # return render_template("image.html", show_img_paths=show_img_paths, result_num=result_num, image_names=image_names)
        return render_template("image.html", result_num=result_num, image_names=image_names)

    else:
        return 404
        # return str(result)


if __name__ == '__main__':
    # print(app.url_map)
    app.run(host='0.0.0.0', debug=False, port=3367)
