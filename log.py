#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import time

def log(*args, **kwargs):
    f = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    with open('spider/logs/log.txt', 'a') as f:
        print('============================================', file=f)
        print(dt, *args, file=f, **kwargs)
        print('============================================', file=f)
        print('', file=f)
