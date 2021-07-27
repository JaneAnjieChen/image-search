
import os

id = 0
for img_file in os.listdir('img/'):
        for img in os.listdir('img/' + img_file):
            path = 'img/' + img_file + '/' + img
            add_0 = (6 - len(str(id))) * '0'
            os.rename(path, 'img/' + img_file + '/' + str(img_file) + '_' + add_0 + str(id) + '.' + img.split('.')[1])
            id += 1

