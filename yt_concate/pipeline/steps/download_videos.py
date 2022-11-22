import os
import time
from multiprocessing import Process

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        yt_set = set([found.yt for found in data])
        download_list = []
        for yt in yt_set:
            download_list.append(yt)
        print('video to download = ' , len(yt_set))
        threads_num = os.cpu_count()
        data_equla_parts = self.func(download_list, threads_num)
        processes = []

        for core in range(threads_num):
            print('registering process %d' % core)
            processes.append(Process(target=self.download_videos, args=(data_equla_parts[core], utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
        end = time.time()
        print('Took', end - start, 'seconds to download videos')

        # for yt in yt_set:
        #     url = yt.url
        #
        #     if utils.video_file_exists(yt):
        #         print(f'found existing video file for {url}, skipping')
        #         continue
        #
        #     print('downloading', url)
        #     YouTube(url).streams.get_highest_resolution().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4' )
        #     print(url, 'download completed')

        return data

    @staticmethod
    def func(data, n):
        count = (len(data) // n) + 1
        data_equla_parts = []
        for i in range(0, len(data), count):
            data_equla_parts.append(data[i:i + count])

        return data_equla_parts

    def download_videos(self, sub_data, utils):
        for yt in sub_data:
            url = yt.url

            if utils.video_file_exists(yt):
                print(f'found existing video file for {url}, skipping')
                continue

            print('downloading', url)
            YouTube(url).streams.get_highest_resolution().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')
            print(url, 'download completed')