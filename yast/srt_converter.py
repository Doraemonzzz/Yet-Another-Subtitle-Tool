# coding: utf-8

import os
import argparse
import io
import sys

from tqdm import tqdm
from vtt_to_srt.vtt_to_srt import vtt_to_srt, vtts_to_srt

from .utils import get_sub_file

def main_func(path):
    """
    整体流程
    """
    if os.path.isfile(path):
        vtt_to_srt(path)
    else:
        for file in tqdm(get_sub_file(path, ["vtt"])):
            vtt_to_srt(file)

def main():
    # 设置输出编码为utf8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="字幕文件夹路径"
    )

    args = parser.parse_args()
    path = args.path
    
    main_func(path)

    # if os.path.isfile(path):
    #     vtt_to_srt(path)
    # else:
    #     for file in tqdm(get_sub_file(path, ["vtt"])):
    #         vtt_to_srt(file)

if __name__ == "__main__":
    main()