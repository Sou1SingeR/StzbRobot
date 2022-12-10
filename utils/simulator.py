from PIL import Image
from pyautogui import locateOnScreen, moveTo, locateCenterOnScreen
from time import sleep


def get_simulator_status():
    # 基准窗口宽度
    STD_WIDTH = 1280

    window_start = locateOnScreen('./images/common/window_start.png', confidence=.95)
    window_end = locateOnScreen('./images/common/window_end.png', confidence=.95)

    print(window_start, window_end)

    left = window_start.left
    right = window_end.left
    top = window_start.top + window_start.height
    bottom = window_end.top + window_end.height

    sleep(1)
    moveTo(left, top, 1)
    moveTo(right, bottom, 1)

    # 缩放比例
    scale = (right - left) / STD_WIDTH

    return left, right, top, bottom, scale


def f():
    left, right, top, bottom, scale = get_simulator_status()
    # accelerator_icon = locateCenterOnScreen


if '__main__' == __name__:
    f()
