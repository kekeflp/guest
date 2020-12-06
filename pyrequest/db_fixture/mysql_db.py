from pymysql import connect, cursors
import pymysql.err
import os
import configparser as cparser

# 读取配置文件
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace("\\", "/")
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
user = cf.get("mysqlconf", "user")
pwd = cf.get("mysqlconf", "password")
db = cf.get("mysqlconf", "db_name")


# 封装dbhelper
class DB:
    def __init__(self):
        try:
            self.conn = connect(host=host,
                                port=int(port),
                                user=user,
                                password=pwd,
                                db=db,
                                charset="utf8mb4",
                                cursorclass=cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        sql = "delete from %s ;" % (table_name)
        with self.conn.cursor() as cursor:
            cursor.execute("set foreign_key_checks=0;")
            cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ",".join(table_data.keys())
        value = ",".join(table_data.values())
        sql = "insert into %s ( %s ) values ( %s );" % (table_name, key, value)
        print(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DB()
    table_name = "sign_event"
    data = {
        "id": 12,
        "name": "红米",
        "limit": 2000,
        "status": 1,
        "address": "北京会展中心",
        "start_time": "2020-12-07 02:25:00"
    }
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()