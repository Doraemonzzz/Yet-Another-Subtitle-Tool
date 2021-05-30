# coding: utf-8

import os
import argparse

from tqdm import tqdm
from vtt_to_srt.vtt_to_srt import vtt_to_srt, vtts_to_srt

from .utils import get_sub_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="字幕文件夹路径"
    )

    args = parser.parse_args()
    path = args.path

    if os.path.isfile(path):
        vtt_to_srt(path)
    else:
        for file in tqdm(get_sub_file(path, ["vtt"])):
            vtt_to_srt(file)

    # if os.path.isdir(path):
    #     vtts_to_srt(path, rec=True)
    # else:
    #     vtt_to_srt(path)

if __name__ == "__main__":
    main()