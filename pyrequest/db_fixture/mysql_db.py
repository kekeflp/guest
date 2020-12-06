import pymysql
import pymysql.err
import os

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace("\\", "/")
file_path = base_dir + "/db_config.ini"
