# -*- coding: utf-8 -*-
"""
Version 0.0.0
- created by Yueran
- Add basic functions countBacklog, findOptimalSpeed, 
  findCurrSpeed, binarySearch, countExtend, findOptimalSpeed_constraint
- Add data and estimated demands
"""

import pandas as pd
from collections import deque
import numpy as np

data = pd.read_excel('demands.xlsx',index_col = 0)
summary = pd.read_excel('summary.xlsx', index_col = 0)


# Ignoring the 4-week constraints
def countBacklog(series, production):
    total = 0
    for i in series:
        total += i
        total -= production
        total = max(0, total)
    return total

def findCurrentSpeed(data, backlog):
    currSpeed = []
    for col in data.columns:
        tmp = data[col]
        currSpeed.append(binarySearch(tmp, backlog[col], countBacklog))
    return currSpeed
        
        
def binarySearch(series, target, func):
    left, right = 0, max(series)
    while left + 1< right:
        mid = (left + right) // 2
        if func(series, mid) <= target:
            right = mid
        else:
            left = mid
    print(left, right)
    if func(series, right) <= target:
        return right
    return left
            
            

def findOptimalSpeed(data):
    OptSpeed = []
    for col in data.columns:
        print(col)
        tmp = data[col]
        OptSpeed.append(binarySearch(tmp, 0, countBacklog))
    return OptSpeed

backlog = summary[summary.columns[2]]

curr = findCurrentSpeed(data, backlog)
opt = findOptimalSpeed(data)
Profit_est_curr = np.array(curr).dot(summary[summary.columns[-2]] - summary[summary.columns[-1]])
Profit_est_opt = np.array(opt).dot(summary[summary.columns[-2]] - summary[summary.columns[-1]])
TotalProfit_curr = (summary[summary.columns[0]] - backlog).dot(summary[summary.columns[-2]] - summary[summary.columns[-1]])

# TODO : Can calculate profit weekly using the estimated speed

# Add 4-week constraint
def countExtend(series, production):
    curr = deque(series[0:4])
    total = 0
    for i in range(4):
        tmp = production
        for j in range(i):
            tmpp = min(curr[j], tmp)
            curr[j] = max(0, curr[j] - tmpp)
            tmp -= tmpp
    
    for i in range(4, len(series)):
        total += curr.popleft()
        curr.append(series[i])
        tmp= production
        for j in range(4):
            tmpp = min(curr[j], tmp)
            curr[j] = max(0, curr[j] - tmpp)
            tmp -= tmpp
    return total

def findOptimalSpeed_constraint(data):
    OptSpeed = []
    for col in data.columns:
        print(col)
        tmp = data[col]
        OptSpeed.append(binarySearch(tmp, 0, countExtend))
    return OptSpeed

opt_constraint = findOptimalSpeed_constraint(data)
            
