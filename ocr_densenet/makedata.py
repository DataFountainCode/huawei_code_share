#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 14:33:52 2019

@author: tcd
"""
import os
import cv2
import pandas as pd
train_csv = '/data/chinese/train_lable.csv'
targetpath = '/home/tcd/ocr_densenet/data/train/'
datapath = '/data/chinese/train_dataset/'
with open(train_csv, 'r') as f:
    for ff in os.listdir(targetpath):
        os.remove(targetpath+ff)
    print('removed')
    ii = 0
    name = []
    filename = []
    for line in f.readlines():
        l = line.strip().split(',')
        if l[-1] == 'text':
            continue
        roi = []
        point = []
        for i in range(1, 9):
            l[i] = int(float(l[i]))
            point.append(l[i])
            if i % 2 == 0:
                roi.append(point)
                point = []
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
        target = str(ii) + 'to' + l[0]
        cv2.imwrite(targetpath + target, im)
        name.append(l[-1].decode('utf-8'))
        filename.append(target.decode('utf-8'))
        ii+=1
    print('image croped in...', datapath)
    
train = pd.DataFrame(columns=['name', 'content'])
train['name'] = filename
train['content'] = name
train.to_csv('/home/tcd/ocr_densenet/files/train.csv', header=True, index=None, encoding='utf-8')
