#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 14:33:52 2019

@author: tcd
"""
import os
import cv2
import pandas as pd

# make test data
datapath = '/data/chinese/test_dataset/'
input_file = '/home/tcd/EAST/output.txt'
output_file = '/home/tcd/ocr_densenet/submission.csv'
testpath = '/home/tcd/ocr_densenet/data/dataset/test/'
submit_example = '/home/tcd/submit_example.csv'
ifmax = True
lists = []

names=['filename', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'text']
ex = pd.read_csv(submit_example)
ex = ex.drop(names[1:], axis=1)
f = pd.read_csv(input_file, names=names[:-1], encoding='utf-8')
f['filename'] = f['filename']+'.jpg'
ex.columns = ['filename']
ex = pd.merge(ex, f, how='left', on=['filename'])
ex = ex.fillna('None')
ex['target_file']=[str(x)+'to' for x in ex.index] + ex['filename']
ex.to_csv(output_file, header=True, index=None, encoding='utf-8')

with open(output_file, 'r') as f:
    for ff in os.listdir(testpath):
        os.remove(testpath+ff)
    print('removed')
    for line in f.readlines():
        l = line.strip().split(',')
        if l[-1] == 'target_file' or l[-1] == 'None' or l[1] == 'None':
            continue
        roi = []
        point = []
        for i in range(1, 9):
            l[i] = int(float(l[i]))
            point.append(l[i])
            if i % 2 == 0:
                roi.append(point)
                point = []
        if ifmax:
            xmin = min([roi[x][0] for x in range(4)])
            xmax = max([roi[x][0] for x in range(4)])
            ymin = min([roi[x][1] for x in range(4)])
            ymax = max([roi[x][1] for x in range(4)])
            if xmin < 0:
                xmin = 0
            if ymin < 0:
                ymin = 0
        im = cv2.imread(datapath + l[0])
        im = im[ymin:ymax, xmin:xmax]
        cv2.imwrite(testpath + l[-1], im)
    print('image croped in...', testpath)
print('test dataset done...')
