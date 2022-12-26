import random
from scipy.special import comb

# 率土之滨非欧玩家比例
star_5_rate = 0.12
try_count = 20
ratio_0 = 0
sum = 1

for i in range(try_count + 1):
    possible_cases = comb(try_count, i)
    ratio = star_5_rate ** i * (1 - star_5_rate) ** (try_count - i) * comb(try_count, i)
    if i == 1:
        ratio += ratio_0
    if i == 0:
        ratio_0 = ratio
    else:
        print('征服卡包抽到{0:2}个五星的概率：{1:9.6f}%，抽到至少{0:2}个五星的概率：{2:9.6f}%'.format(i, ratio*100, sum*100))
        sum -= ratio

print('\n\n')

star_5_rate = 0.12
try_count = 10
sum = 1
for i in range(try_count + 1):
    possible_cases = comb(try_count, i)
    ratio = star_5_rate ** i * (1 - star_5_rate) ** (try_count - i) * comb(try_count, i)
    print('活动卡包抽到{0:2}个五星的概率：{1:9.6f}%，抽到至少{0}个五星的概率：{2:10.6f}%'.format(i, ratio*100, sum*100))
    sum -= ratio

try_count = 270
ratio = 0.1
count = 0
for j in range(100000):
    sum = 0
    for i in range(try_count):
        if random.random() < ratio:
            sum += 1
    if sum / try_count > 0.14:
        count += 1
print(count, count / 100000)


