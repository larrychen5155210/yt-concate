import getopt
import sys

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search_caption import SearchCaption
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_videos import EditVideos
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils

CHANNEL_ID = 'UCgFvT6pUq9HLOvKBYERzXSQ'


def print_usage():
    print('python main.py OPTIONS')
    print('OPTIONS: ')
    print('{:>6} {:<15}{}'.format('-h', '--help', 'Print usage'))
    print('{:>6} {:<15}{}'.format('-i', '--channel__id', 'Channel id of the Youtube channel to download'))
    print('{:>6} {:<15}{}'.format('-w', '--search_word', 'The word you want to search in captions you downloaded'))
    print('{:>6} {:<15}{}'.format('-l', '--limit', 'How many videos that you want to edit'))


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'slap ',
        'limit': 10
    }

    short_opts = 'hi:w:l:'
    long_opts = 'help channel_id= search_word= limit='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-i', '--channel_id'):
            inputs['channel_id'] = arg
        elif opt in ('-w', '--search_word'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            inputs['limit'] = arg

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        SearchCaption(),
        # DownloadVideos(),
        # EditVideos(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
