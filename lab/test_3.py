import pendulum
import pandas as pd
import time
from PIL import Image
import pyautogui
import base
import sys
import random
from scipy.special import comb, perm


candidates = [
    '明皇',
    '纹龙',
    '劉備',
    '情话诉给山鬼',
    '伏辰',
    '凛鹰天下',
    '长安',
    '唐离兮',
    '劍丨淡月',
    '染歌',
    '扶苏',
    '沐丨哀',
    'lin',
    # '沐丨丰登',
    # '帝临九天',
]

res = []

for i in range(len(candidates)):
    res.append(random.choice(candidates))
    candidates.remove(res[i])

print(res)
