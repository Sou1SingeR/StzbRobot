
import pandas as pd
import pendulum
import time
import pyautogui
import base

if True:
    alliance = '天道何方'
    city = '陭氏'
    center_x = 491
    center_y = 689
    radius = 4

    image_temp_path = "./images/fortress_info.png"
    data_excel_path = "./fortress_stat/要塞统计表.xlsx"

    ok = pyautogui.confirm(text='确认开始？', title='确认', buttons=['OK', 'Cancel'])
    if not ok:
        exit(1)
    now = pendulum.now().format('MM-DD HH:mm')
    print("开始统计       当前时间：" + now)

# 获取统计范围
stat_region_x = []
stat_region_y = []
print(center_x, center_y, 'r:' + str(radius))

for i in range(-radius, radius + 1):
    for j in range(-radius, radius + 1):
        stat_region_x.append(center_x + i)
        stat_region_y.append(center_y + j)

# 获取要塞信息
is_first_cycle = True
summary_image = None
for i in range(len(stat_region_x)):
    x = stat_region_x[i]
    y = stat_region_y[i]

    pyautogui.moveTo(800, 90, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()

    pyautogui.moveTo(690, 530, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.typewrite(str(x))
    pyautogui.moveTo(860, 50, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()

    pyautogui.moveTo(760, 530, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.typewrite(str(y))
    pyautogui.moveTo(860, 50, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()

    pyautogui.moveTo(860, 530, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()

    time.sleep(1.5)
    pyautogui.moveTo(465, 290, 0.1, pyautogui.easeOutQuad)
    pyautogui.click()

    region = (240, 270, 90, 45)
    time.sleep(0.5)
    image_current = pyautogui.screenshot(region=region)

    if is_first_cycle:
        summary_image = image_current
        is_first_cycle = False
    else:
        summary_image = base.image_concat(summary_image, image_current)

text_list = base.get_text(summary_image)
print(text_list)






