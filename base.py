import time
import pyautogui
from PIL import Image
from aip import AipOcr


def get_text(image):
    # 百度AI SDK配置
    APP_ID = '15593107'
    API_KEY = 'orTdOYk2EORRQGIiL7Ab1iky'
    SECRET_KEY = 'uEkRcs5j0XNr5KiA41Sz8ERqo0hhtPVL'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    # 截图存放目录
    image_temp_path = "./images/temp.png"

    image.save(image_temp_path)

    with open(image_temp_path, 'rb') as fp:
        content = fp.read()
    text_info = aipOcr.basicAccurate(content, options)
    text_list = []
    # print(text_info)
    for i in text_info['words_result']:
        text_list.append(i['words'])

    return text_list


def point_region(region):
    pyautogui.moveTo(region[0], region[1])
    time.sleep(0.5)
    pyautogui.moveTo(region[0] + region[2], region[1] + region[3])


def image_concat(image_a, image_b):
    width, height = image_a.size
    width2, height2 = image_b.size
    assert(width == width2)

    target = Image.new('RGB', (width, height + height2))
    target.paste(image_a, (0, 0))
    target.paste(image_b, (0, height))

    return target

