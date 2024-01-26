from utils import ocr
from utils import image
from utils import operation
import pyautogui
import time
import pandas as pd


class SiegeCrawler:
    # ocr 区域相对于标志物的 delta_w, delta_h, w, h
    _name_offset = (-790, -2, 175, 32)
    _time_offset = (-225, -50, 220, 32)
    _window_marker_path = './images/siege/window_marker.png'
    _report_marker_path = './images/siege/report_marker.png'
    _blank_marker_path = './images/siege/blank_marker.png'
    _test_image_path = './images/siege/test.png'
    _data_excel_path = './excel/siege/temp.xlsx'

    def run(self):
        ocr_blocks = self._get_screenshots()
        ocr_results = self._get_ocr_results(ocr_blocks)
        stat_dict = self._get_stat_dict(ocr_results)

    def _get_screenshots(self):
        scroll_start_offset = (600, 600)
        title_area = pyautogui.locateOnScreen(self._window_marker_path, confidence=.80)
        scroll_start = (title_area.left + scroll_start_offset[0], title_area.top + scroll_start_offset[1])
        ocr_blocks = []
        reach_bottom = False
        while True:
            report_markers = list(pyautogui.locateAllOnScreen(self._report_marker_path, confidence=.80))
            assert len(report_markers) == 2
            for report_marker in report_markers:
                pyautogui.moveTo(scroll_start)
                pyautogui.mouseDown()
                name_pos = (report_marker.left + self._name_offset[0], report_marker.top + self._name_offset[1], self._name_offset[2], self._name_offset[3])
                time_pos = (report_marker.left + self._time_offset[0], report_marker.top + self._time_offset[1], self._time_offset[2], self._time_offset[3])
                name_img = pyautogui.screenshot(region=name_pos)
                time_img = pyautogui.screenshot(region=time_pos)
                # assert name_pos[1] + name_pos[3] > 0
                ocr_blocks.extend([name_img, time_img])

            scroll_distance = report_markers[0][1] - title_area.top + 0
            pyautogui.moveTo(scroll_start[0], scroll_start[1] - scroll_distance)
            if reach_bottom:
                pyautogui.mouseUp()
                return ocr_blocks

            time.sleep(0.5)
            try:
                pyautogui.locateOnScreen(self._blank_marker_path, confidence=.80)
                pyautogui.mouseUp()
                reach_bottom = True
            except ImageNotFoundException:
                pyautogui.mouseUp()
                continue

    def _get_ocr_results(self, ocr_blocks):
        start_time = time.time()
        i = 0
        step = 20
        ocr_results = []
        while True:
            if i >= len(ocr_blocks):
                break
            ocr_img = image.images_concat(ocr_blocks[i: i + step], 2)
            texts = ocr.get_text(ocr_img)
            assert len(texts) == step
            ocr_results.extend(texts)
            i += step
        print(f'It costs {time.time() - start_time} s for OCR service.')
        return ocr_results

    def _get_stat_dict(self, ocr_results):
        # 最后 1~2 个可能重复
        if len(ocr_results) >= 8 and ocr_results[-4] == ocr_results[-8] and ocr_results[-3] == ocr_results[-7] \
                                 and ocr_results[-2] == ocr_results[-6] and ocr_results[-1] == ocr_results[-5]:
            ocr_results = ocr_results[:-4]
        if len(ocr_results) >= 8 and ocr_results[-4] == ocr_results[-6] and ocr_results[-3] == ocr_results[-5]:
            ocr_results = ocr_results[:-4] + ocr_results[-2:-1]
        names = [name for idx, name in enumerate(ocr_results) if idx % 2 == 0]
        stat_dict = {}
        for name in names:
            stat_dict[name] = stat_dict.get(name, 0) + 1

    def _save_dict_to_excel(self, stat_dict):
        df = pd.DataFrame({'游戏名': list(stat_dict.keys()), '攻击次数': list(stat_dict.values())})
        df = df.sort_values(by=['攻击次数'], ascending=False)
        df.to_excel(self._data_excel_path, index=False)

    def test(self):
        report_marker = pyautogui.locateOnScreen(self._report_marker_path, grayscale=False, confidence=.95)
        name_pos = (report_marker.left + self._name_offset[0], report_marker.top + self._name_offset[1], self._name_offset[2], self._name_offset[3])
        time_pos = (report_marker.left + self._time_offset[0], report_marker.top + self._time_offset[1], self._time_offset[2], self._time_offset[3])
        name_img = pyautogui.screenshot(region=name_pos)
        time_img = pyautogui.screenshot(region=time_pos)
        ocr_img = image.images_concat([name_img, time_img], 2)
        ocr_img.save(self._test_image_path)


if '__main__' == __name__:
    siege_crawler = SiegeCrawler()
    siege_crawler.run()
    # siege_crawler.test()
