import time
import pyautogui


def scroll_down(start, end):
    time.sleep(0.1)
    pyautogui.moveTo(start[0], start[1])
    time.sleep(0.1)
    pyautogui.dragTo(end[0], end[1], 5, pyautogui.easeOutQuad, button='left')



