import time

from pytube import YouTube
from bs4 import BeautifulSoup

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('downloading caption for', url)
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue
            try:
                source = YouTube(url)
                en_caption = source.captions.get_by_language_code('a.en')
                xml = en_caption.xml_captions
                en_caption_srt =self.xml2srt(xml)
                # print(en_caption_srt)
            except AttributeError:
                print('AttributeError when downloading caption for', url)
                continue

            text_file = open(utils.get_caption_filepath(url), "w", encoding='utf-8')
            text_file.write(en_caption_srt)
            text_file.close()

        end = time.time()
        print('took', end-start, 'seconds')



    @staticmethod
    def xml2srt(text):
        soup = BeautifulSoup(text)  # 使用 BeautifulSoup 轉換 xml
        ps = soup.findAll('p')  # 取出所有 p tag 內容

        output = ''  # 輸出的內容
        num = 0  # 每段字幕編號
        for i, p in enumerate(ps):
            try:
                a = p['a']  # 如果是自動字幕，濾掉有 a 屬性的 p tag
            except:
                try:
                    num = num + 1  # 每段字幕編號加 1
                    text = p.text  # 取出每段文字
                    t = int(p['t'])  # 開始時間
                    d = int(p['d'])  # 持續時間

                    h, tm = divmod(t, (60 * 60 * 1000))  # 轉換取得小時、剩下的毫秒數
                    m, ts = divmod(tm, (60 * 1000))  # 轉換取得分鐘、剩下的毫秒數
                    s, ms = divmod(ts, 1000)  # 轉換取得秒數、毫秒

                    t2 = t + d  # 根據持續時間，計算結束時間
                    if t2 > int(ps[i + 1]['t']): t2 = int(ps[i + 1]['t'])  # 如果時間算出來比下一段長，採用下一段的時間
                    h2, tm = divmod(t2, (60 * 60 * 1000))  # 轉換取得小時、剩下的毫秒數
                    m2, ts = divmod(tm, (60 * 1000))  # 轉換取得分鐘、剩下的毫秒數
                    s2, ms2 = divmod(ts, 1000)  # 轉換取得秒數、毫秒

                    output = output + str(num) + '\n'  # 產生輸出的檔案，\n 表示換行
                    output = output + f'{h:02d}:{m:02d}:{s:02d},{ms:03d} --> {h2:02d}:{m2:02d}:{s2:02d},{ms2:03d}' + '\n'
                    output = output + text + '\n'
                    output = output + '\n'
                except:
                    pass

        return output


