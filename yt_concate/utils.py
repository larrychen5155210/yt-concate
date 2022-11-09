import os

from yt_concate.settings import DOWNLOADS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import CAPTIONS_DIR



class Utils:
    def __ini__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR,exist_ok=True)
        os.makedirs(CAPTIONS_DIR,exist_ok=True)

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + '.txt')

    def video_list_file_exist(self, channel_id):
        path = self.get_video_list_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def caption_file_exists(self, yt):
        path = yt.get_caption_filepath()
        return os.path.exists(path) and os.path.getsize(path) > 0

    def video_file_exists(self, yt):
        path = yt.get_video_filepath()
        return os.path.exists(path) and os.path.getsize(path) > 0