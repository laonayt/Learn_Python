#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool, cpu_count

class Test:
    print(cpu_count())

    def start(self,idx):
        print('start' + idx)

def run(fn):
    print(fn)

if __name__ == '__main__':
    arr = [x for x in range(30)]

    pool = Pool(10)
    pool.map(run,arr)

    pool.close()
    pool.join()


