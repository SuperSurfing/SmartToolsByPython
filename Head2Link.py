#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import re

def multi_string_link(array_head):
    lower_head = reduce(lambda x, y: x.lower() + '_' + y.lower(), array_head)
    common_head = reduce(lambda x, y: x + ' ' + y, array_head)
    return '[' + common_head + '](#' + lower_head + ')'

def single_string_link(head):
    return '[' + head + '](#' + head.lower() + ')'

if __name__ == '__main__':
    print('start to convert markdown head...')

    while True :
        raw_head = input('raw head : ')
        if not raw_head :
            break
        array_head = raw_head.split('_')
        #array_head = re.split(r'[_\s]', raw_head)
        if len(array_head) > 1:
            print(multi_string_link(array_head))
        else:
            print(single_string_link(array_head[0]))