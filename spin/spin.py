from time import sleep
from utils.operation import robust_operation
from utils.simulator import get_simulator_status
import pandas as pd
import pyautogui
import json


def get_base_operation_list():
    return [
        ('click', '切换至模拟器窗口', './images/common/simulator.png', 0, 1, 1, 0.9),
        ('click', '打开 99 加速器', './images/common/accelerator.png', 0, 1, 1, 0.9),
        ('click', '点击加速按钮', './images/common/jiasu.png', 1, 0.5, 10, 0.8),
        ('click', '点击开始游戏', './images/common/game_start.png', 20, 2, 10, 0.9, './images/common/helmet.png'),
    ]


def get_account_operation_list(account, password):
    return [
        ('click', '点击头盔（打开账号设置）', './images/common/helmet.png', 1, 1, 10, 0.9, './images/common/switch_account.png'),
        ('click', '点击切换账号', './images/common/switch_account.png', 0, 1, 10, 0.9),
        ('scroll', '向上滚动', './images/common/facebook.png', 0.5, 1, 10, 0.9, None, (0, -100, 0.5, pyautogui.easeOutQuad)),
        ('click', '点击引继账号', './images/common/inherit.png', 0, 1, 10, 0.9),
        ('click', '点击引继码输入框', './images/common/inherit_code.png', 2, 0.5, 10, 0.9),
        ('write', '输入引继码', account, 0.5),
        ('click', '点击引继密码输入框', './images/common/inherit_password.png', 0, 1, 10, 0.9),
        ('write', '输入引继密码', password, 0),
        ('click', '引继确认', './images/common/inherit_confirmation.png', 1, 1, 10, 0.9),
        ('click', '引继成功', './images/common/inherit_success.png', 1, 1, 10, 0.9),
        ('click', '点击头盔（打开账号设置）', './images/common/helmet.png', 1, 1, 10, 0.9),
        ('click', '点击引继码生成', './images/common/inherit_generating.png', 1, 1, 10, 0.9),
        ('scroll', '向上滚动', './images/common/five_points.png', 1, 1, 10, 0.9, None, (0, -250, 0.3, pyautogui.easeOutQuad)),
        ('click', '点击密码设置输入框', './images/common/password_setting.png', 0, 1, 10, 0.9),
        ('write', '输入新密码', password, 0),
        ('click', '点击密码重复输入框', './images/common/password_repeating.png', 0, 1, 10, 0.9),
        ('write', '再次输入新密码', password, 0),
        ('click', '生成引继码成功', './images/common/inherit_generating_success.png', 0, 1, 10, 0.9),
        ('click', '生成引继码确认', './images/common/inherit_generating_confirm.png', 0, 1, 10, 0.9),
        ('click', '关闭账号设置界面', './images/common/close_helmet.png', 0, 1, 10, 0.9),
    ]


def get_main_operation_list(server_img, name_img):
    return [
        ('click', '点击变更服务器', './images/common/switch_server.png', 0.5, 1, 10, 0.9),
        ('click', '选择服务器', server_img, 1, 0.5, 10, 0.85),
        ('click', '确认服务器', './images/common/confirm.png', 0, 1, 10, 0.9),
        ('click', '进入游戏', './images/common/enter_game.png', 1, 0.5, 10, 0.9),
        ('click', '选择角色', name_img, 0.5, 0.5, 10, 0.9),
        ('click', '确认角色', './images/common/confirm_role.png', 0, 0.5, 10, 0.9),
        # ('click', '确认登录奖励', './images/common/confirm.png', 20, 1, 10, 0.9),
        # ('click', '关闭登录奖励', './images/common/reward_close.png', 0, 1, 10, 0.9),
        ('click', '点击召募', './images/spin/recruit.png', 10, 2, 15, 0.9),
        ('click', '点击名将', './images/spin/famous_general.png', 0, 1, 10, 0.9),
        ('click', '点击免费招募', './images/spin/free_recruit.png', 0, 1, 10, 0.9),
        ('conditional_click', '点击确定', './images/spin/recruit_confirm.png', 1, 1, 10, 0.9, None, ('./images/spin/recruit_confirm.png')),
        ('click', '点击 cost 图标', './images/spin/cost.png', 0, 1, 10, 0.9, './images/spin/close_recruit.png'),
        ('click', '关闭抽卡结果界面', './images/spin/close_recruit.png', 0, 1, 10, 0.9),
        ('click', '关闭招募界面', './images/spin/close_recruit.png', 0, 1, 10, 0.9),
        ('click', '点击右箭头（菜单扩展）', './images/common/right_arrow.png', 0, 1, 10, 0.8, './images/common/game_setting.png'),
        ('click', '点击左箭头（UI bug）', './images/common/left_arrow.png', 0, 1, 10, 0.8, './images/common/game_setting.png'),
        ('click', '点击设定', './images/common/game_setting.png', 0, 1, 10, 0.9),
        ('click', '退出登录', './images/common/back_to_login.png', 0, 1, 10, 0.9),
    ]


def get_meta_info():
    meta_info = pd.read_excel('./excel/spin/config.xlsx')
    meta_info.fillna(False, inplace=True)
    meta_dict = {}
    for idx, row in meta_info.iterrows():
        if row['暂停'] is not False:
            continue
        if row['客户端'] != '日服':
            continue

        if row['账号'] not in meta_dict.keys():
            meta_dict[row['账号']] = {
                'password': row['密码'],
                'role': [],
            }
        meta_dict[row['账号']]['role'].append({
            'server': row['服务器'],
            'name': row['角色'],
            'half': row['半价']
        })
    return meta_dict


def run():

    # for operation in get_base_operation_list():
    #     robust_operation(*operation)

    for account in meta_dict.keys():
        password = str(meta_dict[account]['password'])
        for operation in get_account_operation_list(account, password):
            robust_operation(*operation)

        for role in meta_dict[account]['role']:
            server, name, half = role['server'], role['name'], role['half']
            server_img = './images/login/server_{}.png'.format(server)
            name_img = './images/login/account_{}.png'.format(name)
            for operation in get_main_operation_list(server_img, name_img):
                if name is False and operation[1] in ('选择角色', '确认角色'):
                    continue
                robust_operation(*operation)


if '__main__' == __name__:
    # sleep(2)
    meta_dict = get_meta_info()
    # print(json.dumps(meta_dict, indent=4, ensure_ascii=False, sort_keys=False, separators=(', ', ': ')))
    run()

