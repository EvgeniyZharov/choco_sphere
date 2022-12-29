

host = "127.0.0.1"
user = "a0753797_user_one"
password = "pass123"
database_name = "a0753797_test_one"


import pymysql
# from config import host, user, password

con = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    cursorclass=pymysql.cursors.DictCursor
)
