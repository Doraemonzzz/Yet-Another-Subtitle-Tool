# coding: utf-8

import pysrt
import argparse
import os

from tqdm import tqdm

from .utils import (get_sub_lang, get_sub_type, get_sub_name,
                    gen_sub_name, get_sub_file)

LANGS = ["zh-Hans", "en"]

def srt_merger(srt1, srt2, override):
    """
    合并两种语言的字符
    """
    # 文件名
    name = get_sub_name(srt1)
    lang = get_sub_lang(srt1) + "-" + get_sub_lang(srt2)
    type = "srt"
    srt_name = gen_sub_name(name, lang, type)
    if (os.path.exists(srt_name) and (not override)):
        return
    # 初始化
    subs1 = pysrt.open(srt1)
    subs2 = pysrt.open(srt2)
    # 时间段个数
    n1 = len(subs1)
    n2 = len(subs2)
    i = 0
    j = 0
    newsubs = pysrt.SubRipFile()

    # 生成上中下英字幕
    start = min(subs1[0].start, subs2[0].end)
    end = start
    text = ""
    index = 0

    while (i < n1) and (j < n2):
        end1 = subs1[i].end.ordinal
        text1 = subs1[i].text
        end2 = subs2[j].end.ordinal
        text2 = subs2[j].text

        if (end1 < end2):
            end = end1
            i += 1
        elif (end1 > end2):
            end = end2
            j += 1
        else:
            end = end2
            i += 1
            j += 1

        text = text1 + "\n" + text2
        sub = pysrt.SubRipItem(index=index, start=start, end=end, text=text)
        newsubs.append(sub)

        # 更新
        index += 1
        start = end
    
    # 处理剩余部分
    while (i < n1):
        newsubs.append(subs1[i])
        i += 1
    
    while (j < n2):
        newsubs.append(subs2[j])
        j += 1

    newsubs.save(srt_name)

def get_srt_file(path):
    """
    得到不同版本字幕的对应关系
    dict{
        filename : [srt1, ... , srtn]
    }
    """
    srt_files = get_sub_file(path, ["srt"])
    file_to_srt = dict()
    for srt in srt_files:
        srt_file_name = os.path.basename(srt)
        srt_name = get_sub_name(srt_file_name)
        srt_lang = get_sub_lang(srt_file_name)
        srt_type = get_sub_type(srt_file_name)
        # 忽略合并产生的字幕
        if (srt_lang not in LANGS):
            continue
        if (srt_name not in file_to_srt):
            file_to_srt[srt_name] = []
        # 默认英语放在最后
        if srt_type == "en":
            file_to_srt[srt_name].append(srt)
        else:
            file_to_srt[srt_name].insert(0, srt)
            
    return file_to_srt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="字幕文件夹路径"
    )

    parser.add_argument(
        "-o",
        "--override",
        help="是否覆盖已生成的字幕",
        default=False
    )

    args = parser.parse_args()
    path = args.path
    override = args.override

    if os.path.isdir(path):
        file_to_srt = get_srt_file(path)
        for file in tqdm(file_to_srt):
            srt1 = file_to_srt[file][0]
            srt2 = file_to_srt[file][1]
            srt_merger(srt1, srt2, override)

if __name__ == "__main__":
    main()