import time
import pyautogui
import pyperclip
from time import sleep


def robust_operation(operation, name, content=None, delay=1, interval=1, try_times=1, confidence=0.9, check=None, operation_params=None):
    """
    等待 delay 秒后，反复寻找 img 并依据中心坐标进行操作，每次间隔 interval 秒，最多尝试 n 次
    """
    sleep(delay)
    print('正在尝试操作：{}'.format(name))
    for i in range(try_times):
        try:
            if operation == 'click':
                x, y = pyautogui.locateCenterOnScreen(content, confidence=confidence)
                pyautogui.click(x, y)
            elif operation == 'conditional_click':
                try:
                    print(operation)
                    print(operation[0])
                    pyautogui.locateCenterOnScreen(operation_params, confidence=0.9)
                    x, y = pyautogui.locateCenterOnScreen(content, confidence=confidence)
                    pyautogui.click(x, y)
                except Exception as e:
                    print(e)
                    pass
            elif operation == 'scroll':
                x, y = pyautogui.locateCenterOnScreen(content, confidence=confidence)
                pyautogui.moveTo(x, y)
                left, top, duration, mode = operation_params
                pyautogui.drag(left, top, duration, mode, button='left')
            elif operation == 'write':
                write_keys = ['num' + ch if '0' <= ch <= '9' else ch for ch in content]
                if not write_keys[-1].startswith('num'):
                    write_keys += '\n'
                pyautogui.write(write_keys, interval=0.1)
            else:
                raise Exception('Unknown operation.')

            if check is None:
                return
        except Exception as e:
            print(e)

        if check is not None:
            try:
                pyautogui.locateCenterOnScreen(check, confidence=0.8)
                return
            except Exception as e:
                pass

        if i == try_times - 1:
            raise Exception('已达到最大尝试次数。\n\tOpration: {}\n\tTry times: {}'.format(name, try_times))
        sleep(interval)


def scroll_down(start, end):
    pyautogui.moveTo(start[0], start[1])
    pyautogui.dragTo(end[0], end[1], 0.5, pyautogui.easeOutQuad, button='left')
    time.sleep(0.5)



