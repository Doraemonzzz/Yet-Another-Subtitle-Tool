# coding: utf-8

import os

## subtitle tool
def gen_sub_name(name, lang, type):
    """
    根据文件名, 字幕语种和类型生成字幕文件名
    """
    return ".".join([name, lang, type])

def get_sub_type(subfile):
    """
    获得字幕类型, srt或vtt
    """
    return subfile.split(".")[-1]

def get_sub_lang(subfile):
    """
    获得字幕语种, 例如"zh-Hans", "en"
    """
    return subfile.split(".")[-2]

def get_sub_name(subfile):
    """
    abc.en.srt -> abs
    """
    return ".".join(subfile.split(".")[:-2])

## 文件相关
def get_dir_file(dir):
    """
    获得文件夹中文件
    """
    files = []
    for file in os.listdir(dir):
        new_dir = os.path.join(dir, file)
        if os.path.isdir(new_dir):
            files += get_dir_file(new_dir)
        else:
            files.append(new_dir)
    
    return files

def get_sub_file(dir, sub_type=["srt", "vtt"]):
    """
    获得文件夹中字幕文件
    """
    files = get_dir_file(dir)
    sub_files = []
    for file in files:
        if get_sub_type(file) in sub_type:
            sub_files.append(file)
    
    return sub_files

def mkdir(dir):
    path = os.path.join(os.getcwd(), dir)
    if not os.path.exists(path):
        os.mkdir(path)

## 文本处理
def del_newline(str):
    """
    删除换行
    """
    return " ".join(str.strip().split("\n")).strip()

def get_str_max_overlap(str1, str2):
    """
    返回两段文字的最大重叠长度:
    aabb, abbc -> 3(abb)
    """
    n1 = len(str1)
    n2 = len(str2)
    l = min(n1, n2)
    for i in range(l, -1, -1):
        if (str1[-i:] == str2[:i]):
            break

    return i

def rm_dup(str1, str2):
    """
    删除重复部分, 例如
    "black dog"
    "a black dog is"
    作用后变为
    "black dog"
    "is"
    """
    n1 = len(str1)
    n2 = len(str2)
    if (n1 < n2):
        for i in range(n2 - n1):
            if (str1 == str2[i: i + n1]):
                str2 = str2[i + n1:]
                break
    
    return str2

def get_word(str):
    """
    获得str中单词
    """
    return str.strip().split()

def merge_two_str(str1, str2, l):
    """
    合并字符串
    """
    return str1 + " " + str2[l:]

## list相关
def str_to_list(str):
    """
    将字符串按\n划分为列表
    """
    return str.strip().split("\n")

def list_to_str(list, sym=" "):
    """
    将字符串按sym拼接
    """
    return sym.join(list)

def judge_list_overlap(list1, list2):
    """
    判断list1和list2对应元素是否能够合并, 假设列表长度相同
    ["aa", "bb", "cc"], ["aa", "bb", "cc"] -> True
    ["aab", "bbc", "cc"], ["aba", "bcb", "cc"] -> True
    ["aa"], ["bb"] -> False
    """
    n = len(list1)
    overlap_len = [get_str_max_overlap(list1[i], list2[i]) for i in range(n)]
    flag = True
    for l in overlap_len:
        if l == 0:
            flag = False
            break
    
    return flag, overlap_len

def get_list_max_overlap(list1, list2):
    """
    返回两个列表的最大重合长度以及对应字符串的重合长度
    """
    n1 = len(list1)
    n2 = len(list1)
    l = min(n1, n2)
    for i in range(l, -1, -1):
        flag, overlap_len = judge_list_overlap(list1[-i:], list2[:i])
        if (flag):
            break

    return i, overlap_len

def merge_two_list(list1, list2, l, overlap_len):
    """
    根据匹配关系合并列表
    """
    list1_overlap = list1[-l:]
    list2_overlap = list2[:l]
    
    return list1[:-l] + [merge_two_str(list1_overlap[i], list2_overlap[i], overlap_len[i]) for i in range(l)] + list2[l:]