# coding: utf-8

import argparse
import sys
import io

from . import srt_converter
from . import srt_cleaner
from . import srt_merger

def main():
    # 设置输出编码为utf8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="字幕文件夹路径"
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        help="是否覆盖已生成的字幕",
        default=False
    )

    args = parser.parse_args()
    path = args.path
    overwrite = args.overwrite

    srt_converter.main_func(path)
    srt_cleaner.main_func(path)
    srt_merger.main_func(path + "/clean_srt", overwrite)

    # subprocess.call(f"srt_converter --path {path}")
    # #subprocess.call("srt_converter --path " + dir)
    # subprocess.call(f"srt_clearner --path {path}")
    # subprocess.call(f"srt_merger --path {path}/clean_srt --overwrite {overwrite}")

    # subprocess.call(f"python srt_converter.py --path {dir}")
    # subprocess.call(f"python srt_clearner.py --path {dir}")
    # subprocess.call(f"python srt_merger.py --path {dir}/clean_srt --overwrite {overwrite}")
    
if __name__ == '__main__':
    main()