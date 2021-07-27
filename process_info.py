import os
import pymysql
from AES import encrypt, decrypt
import csv


def projection_write_csv():
    f = open('image_info.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)

    # 映射图片路径
    # 将图片名和映射过的图片路径存成csv文件
    key = '123456_Encrypting'

    for img_file in os.listdir('img/'):
        for img in os.listdir('img/' + img_file):
            path = 'img/' + img_file + '/' + img
            epath = encrypt(key, path)
            # img, epath

            csv_writer.writerow([img, epath])
    f.close()


def get_connection():
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='image_search_db', charset='utf8')
    return connection

def read_csv_to_mysql(filename):
    with open(filename) as f:
        reader = csv.reader(f)

        connection = get_connection()
        cursor = connection.cursor()

        for row in reader:
            args = str(tuple(row))
            sql = 'INSERT INTO image_info values{}'.format(args)

            # 读取有空行
            try:
                cursor.execute(sql)
            except:
                print('{} insertation is unsuccessful.'.format(args))

            print('{} insertation is successful.'.format(args))

        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
#     # projection_write_csv()
#     # # get_connection()
    read_csv_to_mysql('image_info.csv')
