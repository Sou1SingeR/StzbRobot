import time
import pyautogui


def scroll_down(start, end):
    pyautogui.moveTo(start[0], start[1])
    pyautogui.dragTo(end[0], end[1], 0.5, pyautogui.easeOutQuad, button='left')
    time.sleep(0.4)



