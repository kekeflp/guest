import sys
sys.path.append("..")
from .mysql_db import DB

datas = {'''
    测试数据
    '''}


def init_data():
    db = DB()
    for table, data in datas.items:
        db.clear()
        for d in data:
            db.insert(table, d)
    db.close()