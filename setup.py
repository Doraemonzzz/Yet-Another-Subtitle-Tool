# coding: utf-8

from distutils.core import setup

setup(
    name='yast',
    version='0.0.0',
    description='Yet another subtitle tool',
    author='Doraemonzzz',
    author_email='doraemon_zzz@163.com',
    url='none',
    packages=['yast'],
    entry_points={
        'console_scripts': [
            'srt_cleaner=yast.srt_cleaner:main',
            'srt_merger=yast.srt_merger:main',
            'srt_converter=yast.srt_converter:main'
        ],
    },
    install_requires=[
        'vtt_to_srt3>=0.1.8.6',
        'tqdm>=v4.61.0'
    ],
)