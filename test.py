# from datetime import datetime

# date_ = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# print(date_)

from config import database
import pymysql
from pymysql import connections
from pymysql.err import OperationalError

# 连接池配置
pool = connections.Pool(
    host=database["host"],
    user=database["user"],
    password=database['password'],
    database=database['database'],
    autocommit=True,  # 自动提交事务
    max_connections=10  # 最大连接数
)

# 尝试获取连接
try:
    connection = pool.get_connection()
except OperationalError as e:
    print(f"Error: Could not connect to the database. {e}")
    exit(1)

try:
    with connection.cursor() as cursor:
        # 执行 SQL 查询
        sql = "SELECT * FROM clocks"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    # 将连接归还给连接池
    connection.close()
