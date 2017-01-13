#coding=utf8
'''
Created on 2017年1月11日

@author: ZWJ
'''
import time

def is_status_timeout(item): 
#     print item   
    diff = time.time() - time.mktime(time.strptime(str(item.update_date),'%Y-%m-%d %H:%M:%S'))
    return True if diff > 240 else False

def separate_items(items,status=None):
    if status == 'on':
        return list(item for item in items if not is_status_timeout(item))
    elif status == 'off':
        return list(item for item in items if is_status_timeout(item))
    else:
        return items