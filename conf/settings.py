# __author__ = "XYT"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
全局配置文件
 
'''




#本地mysql
db_server_conf={
    'host':'192.168.88.135',
    'port':3306,
    'user':'jack',
    'pwd':'123456',
    'db':'db2',
}

