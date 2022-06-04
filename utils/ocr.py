from time import time
import pyautogui
from PIL import Image
from aip import AipOcr


if True:
    APP_ID = '15593107'
    API_KEY = 'orTdOYk2EORRQGIiL7Ab1iky'
    SECRET_KEY = 'uEkRcs5j0XNr5KiA41Sz8ERqo0hhtPVL'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'detect_direction': 'true',
        'language_type': 'auto_detect',
    }

    # 截图存放目录
    image_temp_path = "./images/temp.png"


def get_text(image):
    t0 = time()
    image.save(image_temp_path)
    with open(image_temp_path, 'rb') as fp:
        content = fp.read()
    text_info = aipOcr.basicAccurate(content, options)
    text_list = []
    print(text_info)
    print('cost: {}s'.format(time() - t0))
    for i in text_info['words_result']:
        text_list.append(i['words'])

    return text_list


def get_text_by_file(image_path):
    t0 = time()
    with open(image_path, 'rb') as fp:
        content = fp.read()
    text_info = aipOcr.basicAccurate(content, options)
    text_list = []
    print(text_info)
    print('cost: {}s'.format(time() - t0))
    for i in text_info['words_result']:
        text_list.append(i['words'])

    return text_list
