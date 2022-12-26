
import pandas as pd
import pendulum
import time
import pyautogui
from aip import AipOcr


if True:
    # 百度AI SDK配置
    APP_ID = '15593107'
    API_KEY = 'orTdOYk2EORRQGIiL7Ab1iky'
    SECRET_KEY = 'uEkRcs5j0XNr5KiA41Sz8ERqo0hhtPVL'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    # 截图、数据表存放目录
    image_temp_path = "./images/temp.png"
    data_excel_path = "./power_stat/势力值统计表————天道何方.xlsx"

    now = pendulum.now().format('MM-DD HH:mm')
    print("开始统计       当前时间：" + now)


def get_text(image_name):
    with open(image_name, 'rb') as fp:
        content = fp.read()
    text_info = aipOcr.basicAccurate(content, options)
    text_list = []
    print(text_info)
    for i in text_info['words_result']:
        text_list.append(i['words'])
    return text_list


def scroll_down():
    time.sleep(0.1)
    pyautogui.moveTo(400, 480)
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.moveTo(400, 200, 0.5, pyautogui.easeOutQuad)
    time.sleep(0.8)
    pyautogui.mouseUp()
    time.sleep(1.5)


name_list = []
power_list = []
end_name = None
pyautogui.confirm(text='确认开始？', title='确认', buttons=['OK', 'Cancel'])

# 从游戏内获取数据
while True:
    # 获取第一行位置
    page_players = pyautogui.locateOnScreen('./images/row_mark.png', grayscale=False, confidence=.90)
    pyautogui.moveTo(425, page_players.top)

    # 截图7行
    region_names = (90, page_players.top, 110, 320)
    region_power = (425, page_players.top, 80, 320)

    image = pyautogui.screenshot(region=region_names)
    image.save(image_temp_path)
    names = get_text(image_temp_path)
    name_list.extend(names)

    image = pyautogui.screenshot(region=region_power)
    image.save(image_temp_path)
    power = get_text(image_temp_path)
    power_list.extend(power)

    # 找到本页最后一个name
    page_end_name = None
    for i in names:
        page_end_name = i

    # 如跟上页重复，补充最底下一行，退出循环
    if end_name is not None and page_end_name == end_name:
        # 最后一行
        time.sleep(2)
        region_names = (90, 480, 110, 30)
        region_power = (425, 480, 80, 30)

        image = pyautogui.screenshot(region=region_names)
        image.save(image_temp_path)
        names = get_text(image_temp_path)
        name_list.extend(names)

        image = pyautogui.screenshot(region=region_power)
        image.save(image_temp_path)
        power = get_text(image_temp_path)
        power_list.extend(power)
        break

    end_name = page_end_name
    scroll_down()

if len(name_list) != len(power_list):
    print(len(name_list), len(power_list))
    print(name_list)
    print(power_list)
    raise Exception('长度不等')

power_dict = {}
for i in range(len(name_list)):
    name = name_list[i].replace('、', '丶')
    power = power_list[i]
    power_dict[name] = power

# 尝试读取上次保存的数据
try:
    base_data = pd.read_excel(data_excel_path)
except:
    print('数据文件不存在，需要初始化')
    base_data = pd.DataFrame({'ID': [], 'increase': []})
    last_col = None
else:
    last_col = list(base_data.columns)[2]
    base_data = base_data.fillna('')

new_data = base_data.copy()
current_power = []
for index, row in new_data.iterrows():
    name = row['ID']

    # 处理power
    if power_dict.get(name) is None:
        # 此人离开了同盟
        power = None
    else:
        power = int(power_dict.pop(name))
    current_power.append(power)

    # 处理increase
    if last_col is not None and power is not None and row[last_col] != '':
        row[last_col] = int(row[last_col])
        row['increase'] = int(power - row[last_col])
    else:
        row['increase'] = None

# 插入新的势力值列
new_data.insert(2, now, current_power)

# 清理离开的人
# new_data = new_data[new_data[now].notnull()]

# 加上新来的人
for key, value in power_dict.items():
    row_dict = {'ID': key, now: value}
    new_data = new_data.append(row_dict, ignore_index=True)

# 排序
new_data = new_data.sort_values(by=['increase'], ascending=True)

new_data.to_excel(data_excel_path, index=False)




