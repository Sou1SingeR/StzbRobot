from utils import ocr
from utils import image
from utils import operation
from collections import Counter
import pyautogui
import time
import pandas as pd


def test():
    t0 = time.time()
    siege_statistics('2022-06-02 21:00:00')
    cost = time.time() - t0
    print('cost: {}s'.format(cost))


def siege_statistics(start_time):
    # ocr 区域相对于标志物的偏移量、宽高
    name_offset = (-770, -7, 175, 30)
    time_offset = (-235, -55, 215, 30)
    # 最小时间
    time_min = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    scroll_start_offset = (600, 600)
    title_area = pyautogui.locateOnScreen('./images/siege/window_marker.png', grayscale=False, confidence=.80)
    scroll_start = (title_area.left + scroll_start_offset[0], title_area.top + scroll_start_offset[1])

    ocr_blocks = []
    user_list = []
    rows = 0
    err = []
    err_time = []
    err_name = []
    while True:
        # 寻找标志物
        report_marker = pyautogui.locateOnScreen('./images/siege/report_marker.png', grayscale=False, confidence=.80)

        name_pos = (report_marker.left + name_offset[0], report_marker.top + name_offset[1], name_offset[2], name_offset[3])
        name_img = pyautogui.screenshot(region=name_pos)
        time_pos = (report_marker.left + time_offset[0], report_marker.top + time_offset[1], time_offset[2], time_offset[3])
        time_img = pyautogui.screenshot(region=time_pos)
        ocr_blocks.append(name_img)
        ocr_blocks.append(time_img)
        rows += 1

        # 滚动
        scroll_distance = report_marker.top - title_area.top - 80
        scroll_end = (scroll_start[0], scroll_start[1] - scroll_distance)
        operation.scroll_down(scroll_start, scroll_end)
        # time.sleep(1)

        # 每 10 行检测一次时间
        if rows == 10:
            rows = 0
            ocr_img = image.images_concat(ocr_blocks, 2)
            txt = ocr.get_text(ocr_img)
            ocr_blocks = []
            time_over = False
            for i in range(10):
                t_txt = txt[i * 2 + 1].replace(' ', '')
                try:
                    t = time.strptime(t_txt, '%Y/%m/%d%H:%M:%S')
                except Exception as e:
                    err.append(e)
                    err_name.append(txt[i * 2])
                    err_time.append(txt[i * 2 + 1])
                    continue
                if t > time_min:
                    user_list.append(txt[i * 2])
                else:
                    time_over = True
                    break
            if time_over:
                break

    cnt_dict = {}
    for user in user_list:
        cnt_dict[user] = cnt_dict.get(user, 0) + 1
    print(cnt_dict)

    data_excel_path = './excel/siege/siege_{}.xlsx'.format(start_time[:10])
    keys = []
    values = []
    for k, v in cnt_dict.items():
        keys.append(k)
        values.append(v)

    df = pd.DataFrame({'ID': keys, 'cnt': values})
    df = df.sort_values(by=['cnt'], ascending=False)
    df.to_excel(data_excel_path, index=False)

    print(err, err_time, err_name)

