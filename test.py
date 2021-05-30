import os
import pysrt
import random

from vtt_to_srt.vtt_to_srt import vtt_to_srt
from utils import get_sub_name

def vtt_test(path):
    vtt_to_srt(path)

def get_sub_name_test(file):
    print(get_sub_name(file))

def main():
    # path = './test_subtitle/[2019-03-18] 2019-03-14 - Hardness#2 - More on Max-IS, and Max-SAT.en.vtt'
    # vtt_test(path)

    # file = "[2020-12-30] 21.1 Total Variation.zh-Hans.vtt"
    # print(get_sub_name(file))
    # path = "/Users/qinzhen/Desktop/学习/web/django_test"
    # print(os.getcwd())
    # print(os.path.join(os.getcwd(), path))
    subs = pysrt.open("/Users/qinzhen/Desktop/学习/web/Subtitle-Tool/test_subtitle/[2018-01-17] Lecture 1. Introduction to Probabilistic Graphical Models Terminology and Examples.en.srt")
    t = []
    for sub in subs:
        t.append(sub.start)

    print(type(t))
    print(sorted(t))
    print(sorted(random.shuffle(t)))

if __name__ == '__main__':
    main()
