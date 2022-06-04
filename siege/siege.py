from utils import ocr
from utils import image
from utils import operation
import pyautogui
import time


def test():
    # t = '2022/06/02 21:19:08'.replace(' ', '')
    # print(time.strptime(t, '%Y/%m/%d%H:%M:%S'))

    # 滚屏偏移量
    scroll_start_offset = (600, 600)
    scroll_end_offset = (0, -620)
    title_area = pyautogui.locateOnScreen('./images/siege/window_marker.png', grayscale=False, confidence=.80)
    scroll_start = (title_area.left + scroll_start_offset[0], title_area.top + scroll_start_offset[1])
    scroll_end = (scroll_start[0] + scroll_end_offset[0], scroll_start[1] + scroll_end_offset[1])
    operation.scroll_down(scroll_start, scroll_end)


def siege_statistics(start_time):
    # ocr 区域相对于标志物的偏移量、宽高
    name_offset = (-770, -2, 170, 30)
    time_offset = (-235, -50, 210, 30)
    # 最小时间
    time_min = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    ocr_blocks = []
    # for

    # 寻找标志物
    report_marker = pyautogui.locateOnScreen('./images/siege/report_marker.png', grayscale=False, confidence=.80)

    name_pos = (report_marker.left + name_offset[0], report_marker.top + name_offset[1], name_offset[2], name_offset[3])
    name_img = pyautogui.screenshot(region=name_pos)
    time_pos = (report_marker.left + time_offset[0], report_marker.top + time_offset[1], time_offset[2], time_offset[3])
    time_img = pyautogui.screenshot(region=time_pos)
    ocr_blocks.append(name_img)
    ocr_blocks.append(time_img)
    ocr_img = image.images_concat(ocr_blocks, 2)
    ocr_img.save('./images/tmp/3.png')

    txt = ocr.get_text(ocr_img)
    print(txt)


