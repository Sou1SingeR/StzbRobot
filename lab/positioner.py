import pendulum
import pandas as pd
import time
from PIL import Image
import pyautogui
import msvcrt
import sys
import random


def positioner():
    screen_width, screen_height = pyautogui.size()
    print('屏幕尺寸：({}, {})'.format(screen_width, screen_height))

    try:
        while True:
            # 按任意键获取坐标，按 Ctrl + C 退出
            ch = msvcrt.getch()

            x, y = pyautogui.position()
            print('当前坐标: ({}, {}), {}'.format(x, y, str(ch)))
            time.sleep(1)
    except KeyboardInterrupt as e:
        print('结束')


if '__main__' == __name__:
    positioner()
