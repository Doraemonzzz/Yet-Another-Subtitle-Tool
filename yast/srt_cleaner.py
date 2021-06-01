# coding: utf-8

import pysrt
import os
import argparse

from tqdm import tqdm

from .utils import (del_newline, del_newline, get_str_max_overlap, 
                    merge_two_str, str_to_list, list_to_str,
                    get_list_max_overlap, merge_two_list, get_word,
                    rm_dup, get_sub_name, get_sub_lang,
                    mkdir, get_sub_file)


def srt_cleaner(file, dir="clean_srt", maxlen=20, reslen=5):
    """
    对字幕按照字符级拼接, 当当前时间段字幕单词数超过maxlen时, 
    做截断, 保留至少reslen个单词给下个时间段使用。
    结果存储在字幕文件夹下的clean_srt文件夹中。
    """
    ## 初始化
    filename = os.path.basename(file)
    save_dir = os.path.join(os.getcwd(), dir)
    # 生成目录
    mkdir(save_dir)
    # 获得文件名
    path = file
    save_path = os.path.join(save_dir, filename)
    # 判断是否存在
    if os.path.exists(save_path):
        return False
    # 打开字幕
    subs = pysrt.open(path)
    n = len(subs)
    newsubs = pysrt.SubRipFile()
    # 判断是否有重叠
    flag = False
    # 索引
    index = 0

    ## 清理字幕
    # 前一时刻字幕
    prevstart = subs[0].start.ordinal
    prevend = subs[0].end.ordinal
    prevtext = del_newline(subs[0].text)

    for i in range(1, n):
        # 当前时刻字幕
        start = subs[i].start.ordinal
        end = subs[i].end.ordinal
        text = del_newline(subs[i].text)
        # 预处理
        text = rm_dup(prevtext, text)
        # 计算最大重合长度
        l = get_str_max_overlap(prevtext, text)
        newtext = merge_two_str(prevtext, text, l)
        # 最后一轮特殊处理
        if (i == n - 1):
            sub = pysrt.SubRipItem(index=index, start=prevstart, end=end, text=newtext)
            newsubs.append(sub)
            continue

        if (l == 0):
            # 不重合则写入前一时刻字幕
            if (prevtext != ""):
                sub = pysrt.SubRipItem(index=index, start=prevstart, end=prevend, text=prevtext)
                newsubs.append(sub)
                # 更新
                prevstart = start
                prevend = end
                prevtext = text
                index += 1
            else:
                prevend = end
                prevtext = text
        else:
            flag = True
            l = min(len(prevtext), maxlen - reslen)
            # 重合则合并字幕
            prevtext = newtext
            # 获得单词
            word_list = get_word(prevtext)

            # 按照最大字符数量划分
            if len(word_list) > maxlen:
                prevtext = list_to_str(word_list[:l])
                sub = pysrt.SubRipItem(index=index, start=prevstart, end=prevend, text=prevtext)
                newsubs.append(sub)
                # 更新
                prevtext = list_to_str(word_list[l:])
                prevstart = start
                prevend = end
                index += 1
            else:
                prevend = end

    newsubs.save(save_path)

    return flag

def main_func(path):
    """
    整体流程
    """
    if os.path.isfile(path):
        srt_cleaner(path)
    else:
        for file in tqdm(get_sub_file(path, ["srt"])):
            srt_cleaner(file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        help="字幕文件名或字幕目录"
    )

    args = parser.parse_args()
    path = args.path

    main_func(path)
    # if os.path.isfile(path):
    #     srt_cleaner(path)
    # else:
    #     for file in tqdm(get_sub_file(path, ["srt"])):
    #         srt_cleaner(file)
    

if __name__ == "__main__":
    main()
