import pymysql
from config import TOKEN, host, user, password, database_title

TABLES = [
    "users",
    "category",
    "product",
    "orders",
    "sold_pack",
    "ask_answer",
    "user_ticket"
]

con = ""


# CONNECT TO DATABASE

def connecting():
    global con
    try:
        con = pymysql.connect(
            host=host,
            user=user,
            port=3306,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("SUCCESS")
        return True
    except Exception as ex:
        print(ex)
        return False


# CREATE DATABASE

def create_main_db(db_title=database_title):
    try:
        request = f"CREATE DATABASE IF NOT EXISTS {db_title};"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


# CREATE TABLE FOR DATABASE

def create_user_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.users (user_id int UNIQUE,
								 phone VARCHAR(20) UNIQUE,
                                 user_password VARCHAR(20),
                                 user_status VARCHAR(20),
                                 PRIMARY KEY(user_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_category_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.category (category_id int AUTO_INCREMENT,
								 title VARCHAR(20) UNIQUE,
                                 category_description TEXT,
                                 image_link VARCHAR(200),
                                 PRIMARY KEY(category_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_product_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.product (product_id int AUTO_INCREMENT,
								 category_id int,
                                 title VARCHAR(20),
                                 product_description TEXT,
                                 structure TEXT,
                                 price int,
                                 image_link VARCHAR(200),
                                 PRIMARY KEY(product_id),
                                 UNIQUE(title, category_id),
                                 FOREIGN KEY(category_id) REFERENCES category(category_id) ON DELETE CASCADE ON UPDATE CASCADE);"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_orders_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.orders (order_id int AUTO_INCREMENT,
								 user_id VARCHAR(20),
                                 order_date VARCHAR(20),
                                 to_date TEXT,
                                 type_deliver VARCHAR(20),
                                 to_place TEXT,
                                 count_packet int,
                                 user_phone VARCHAR(20),
                                 user_comment VARCHAR(20),
                                 status VARCHAR(50),
                                 PRIMARY KEY(order_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_sold_pack_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.sold_pack (sold_id int AUTO_INCREMENT,
								 order_id int,
								 product_title VARCHAR(100),
                                 count int,
                                 one_price int,
                                 PRIMARY KEY(sold_id),
                                 FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE);"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_ask_answer_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.ask_answer (ask_answer_id int AUTO_INCREMENT,
                                 ask VARCHAR(200) UNIQUE,
                                 answer TEXT,
                                 PRIMARY KEY(ask_answer_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_user_ticket_table(db_title=database_title):
    try:
        request = f"""CREATE TABLE IF NOT EXISTS db_chocosphere.user_ticket (user_ticket_id int AUTO_INCREMENT,
								 user_id VARCHAR(20),
								 ask TEXT,
                                 status VARCHAR(50),
                                 PRIMARY KEY(user_ticket_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


# ADD ELEMENT FOR TABLE IN DATABASE

def add_users_in_table(phone, user_password, user_status="client"):
    try:
        request = """INSERT INTO db_chocosphere.users (phone, user_password, user_status) VALUES (%s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(phone, user_password, user_status)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_admin_in_table(phone, user_password):
    result = add_users_in_table(phone, user_password, user_status="admin")
    return result


def add_category_in_table(title, category_description, image_link):
    try:
        request = """INSERT INTO db_chocosphere.category (title, category_description, image_link) VALUES (%s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(title, category_description, image_link)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_product_in_table(category_id, title, product_description, structure, price, image_link):
    try:
        request = """INSERT INTO db_chocosphere.product (category_id, title, product_description, structure, price, image_link) VALUES (%s, %s, %s, %s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(category_id, title, product_description, structure, price, image_link)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_orders_in_table(user_id, order_date, to_date, type_deliver, to_place, count_packet, user_phone, user_comment, status):
    try:
        request = """INSERT INTO db_chocosphere.orders (user_id, order_date, to_date, type_deliver, to_place, count_packet, user_phone, user_comment, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(user_id, order_date, to_date, type_deliver, to_place, count_packet, user_phone, user_comment, status)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_sold_pack_in_table(order_id, product_title, count, one_price):
    try:
        request = """INSERT INTO db_chocosphere.sold_pack (order_id, product_title, count, one_price) VALUES (%s, %s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(order_id, product_title, count, one_price)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_ask_answer_in_table(ask, answer):
    try:
        request = """INSERT INTO db_chocosphere.ask_answer (ask, answer) VALUES (%s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(ask, answer)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_user_ticket_in_table(user_id, ask, status):
    try:
        request = """INSERT INTO db_chocosphere.user_ticket (user_id, ask, status) VALUES (%s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(user_id, ask, status)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


# UPDATE TABLES FOR DATABASE

def update_phone_user(user_id, new_phone):
    try:
        request = f"UPDATE db_chocosphere.users SET phone = '{new_phone}' WHERE user_id = {user_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()

        return True
    except Exception:
        return False


def update_password_user(user_id, new_password):
    try:
        request = f"UPDATE db_chocosphere.users SET user_password = '{new_password}' WHERE user_id = {user_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()

        return True
    except Exception:
        return False


def update_status_user_ticket(user_ticket_id, new_status):
    try:
        request = f"UPDATE db_chocosphere.user_ticket SET status = '{new_status}' WHERE user_ticket_id = {user_ticket_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()

        return True
    except Exception:
        return False


def update_status_order(order_id, new_status):
    try:
        request = f"UPDATE db_chocosphere.orders SET status = '{new_status}' WHERE order_id = {order_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()

        return True
    except Exception:
        return False

# DELETE ELEMENT FROM TABLE FOR DATABASEf


def del_category_from_table(title):
    try:
        request = f"DELETE FROM db_chocosphere.category WHERE title = '{title}';"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_product_from_table(title, category_id):
    try:
        request = f"DELETE FROM db_chocosphere.product WHERE title = '{title}' and category_id = '{category_id}';"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_ask_answer_from_table(ask):
    try:
        request = f"DELETE FROM db_chocosphere.ask_answer WHERE ask = '{ask}';"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False



#
#
# def del_course_from_table(course_number):
#     try:
#         request = f"DELETE FROM db_chocosphere.user_ticket WHERE course_number = '{course_number}'"
#         with con.cursor() as cur:
#             cur.execute(request)
#             con.commit()
#             return True
#     except Exception:
#         return False


# GET TABLE FROM DATABASE

def get_table(table_title, db_title=database_title):
    if table_title in TABLES:
        request = f"SELECT * FROM {db_title}.{table_title}"
        with con.cursor() as cur:
            cur.execute(request)
        return cur.fetchall()


def get_users_table():
    return get_table(TABLES[0])


def get_category_table():
    return get_table(TABLES[1])


def get_product_table():
    return get_table(TABLES[2])


def get_orders_table():
    return get_table(TABLES[3])


def get_sold_pack_table():
    return get_table(TABLES[4])


def get_ask_answer_table():
    return get_table(TABLES[5])


def get_user_ticket_table():
    return get_table(TABLES[6])


## GET ELEMENT FROM TABLE

def get_elements_table(table_title, elements, db_title=database_title):
    if table_title in TABLES:
        try:
            part_request = ", ".join(elements)
            request = f"SELECT {part_request} FROM {db_title}.{table_title}"
            with con.cursor() as cur:
                cur.execute(request)
            return [True, cur.fetchall()]
        except Exception as ex:
            return [False, ex]


def get_list_category():
    result = get_elements_table(TABLES[1], ["title"])
    if result[0]:
        category_list = [elem["title"] for elem in result[1]]
        return category_list


def get_list_ask():
    result = get_elements_table(TABLES[5], ["ask"])
    if result[0]:
        ask_list = [elem["ask"] for elem in result[1]]
        return ask_list


## GET ELEMENT FROM TABLE ON KEY

def get_elem_for_elem(table_title, elements, condition_1, condition_2, db_title=database_title):
    if table_title in TABLES:
        try:
            part_request = ", ".join(elements)
            request = f"SELECT {part_request} FROM {db_title}.{table_title} WHERE {condition_1} = '{condition_2}';"
            with con.cursor() as cur:
                cur.execute(request)
            return [True, cur.fetchall()]
        except Exception as ex:
            return [False, ex]


def get_id_from_title_category(title):
    result = get_elem_for_elem(TABLES[1], ["category_id"], "title", title)
    if result[0]:
        return result[1][0]["category_id"]
    else:
        return False


def get_from_phone_user(phone):
    result = get_elem_for_elem(TABLES[0], ["*"], "phone", phone)
    if result[0]:
        return result[1][0]
    else:
        return False


def get_from_category_product(category_id):
    result = get_elem_for_elem(TABLES[2], ["*"], "category_id", category_id)
    if result[0]:
        return result[1]
    else:
        return False


def get_from_category_product_title(category_id):
    result = get_elem_for_elem(TABLES[2], ["title"], "category_id", category_id)
    if result[0]:
        product_list = list()
        for elem in result[1]:
            product_list.append(elem["title"])
        return product_list
    else:
        return False


def get_from_ask_answer(ask):
    result = get_elem_for_elem(TABLES[5], ["answer"], "ask", ask)
    if result[0]:
        return result[1][0]["answer"]
    else:
        return False


def get_from_order_sold(order_id):
    result = get_elem_for_elem(TABLES[4], ['product_title', 'count', 'one_price'], "order_id", order_id)
    if result[0]:
        return result[1]
    else:
        return False


def get_actual_user_ticket():
    result = get_elem_for_elem(TABLES[6], ["*"], "status", "ACTUAL")
    if result[0]:
        return result[1]
    else:
        return False


def get_actual_order():
    result = get_elem_for_elem(TABLES[3], ["*"], "status", "ACTUAL")
    if result[0]:
        return result[1]
    else:
        return False


# ADD FUNCTION

def add_new_solds_packs(basket, basket_price, order_id):
    try:
        for elem in basket:
            add_sold_pack_in_table(order_id, elem, basket[elem], basket_price[elem])
        return True
    except Exception:
        return False


# TESTING

print("***"*100)

print(connecting())
# del_all_product_for_category_id(1)

print("***"*100)

print(create_main_db())
print(create_category_table())
print(create_orders_table())
print(create_product_table())
print(create_sold_pack_table())
print(create_user_table())
print(create_user_ticket_table())
print(create_ask_answer_table())

print("***"*100)

user_id = 1
count_product = 3
category_id = 1
all_price = 300
order_id = 1
product_id = 1
count_sold = 4
price = 200

# print(add_users_in_table("+79998887767", "hard_password"))
# print(add_admin_in_table("+79999999999", "hard_password"))
# print(add_category_in_table("category one", "description of the category", "some link for image"))
# print(add_orders_in_table(user_id, "22.22.2222", "33.33.3333", "delivery", "Moscow", count_product, "+71232134", "some text of comment", "ACTUAL"))
# print(add_product_in_table(category_id, "product one", "description of the product", "some material", all_price, "some link"))
# print(add_ask_answer_in_table("what?", "not matter."))
# print(add_sold_pack_in_table(order_id, "some_product", count_sold, price))
# print(add_user_ticket_in_table("some id", "How to do this 2?", "ACTUAL"))

# print("***"*100)

print(get_table(TABLES[0]))
print(get_table(TABLES[1]))
print(get_table(TABLES[2]))
print(get_table(TABLES[3]))
print(get_table(TABLES[4]))
print(get_table(TABLES[5]))
print(get_table(TABLES[6]))

print("***"*100)

# print(get_list_category())
# print(get_id_from_title_category("category one"))
# print(get_from_phone_user("+79999999999"))
# print(del_category_from_table("category one"))
# print(get_from_category_product(5))

print("***"*100)


################################################################################33

#
#
# def sql_start(db_name="new_db.db"):
#
#     conn = sql.connect(db_name)
#     cur = conn.cursor()
#
#     if conn:
#         print("Data Base connected OK.")
#
#     # id, mail, contact, password, status
#     request = "CREATE TABLE IF NOT EXISTS users(" \
#               "id INT PRIMARY KEY NOT NULL, " \
#               "mail TEXT NOT NULL," \
#               "contact TEXT NOT NULL," \
#               "password TEXT NOT NULL," \
#               "status TEXT)"
#     cur.execute(request)
#
#     # id, title, description
#     request = "CREATE TABLE IF NOT EXISTS category_product(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "title TEXT NOT NULL," \
#               "description TEXT NOT NULL," \
#               "image TEXT NOT NULL);"
#     cur.execute(request)
#
#     # id, title, describe, image, price, structure, category_id
#     request = "CREATE TABLE IF NOT EXISTS products(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "title TEXT NOT NULL," \
#               "describe TEXT NOT NULL," \
#               "image TEXT NOT NULL," \
#               "price INT NOT NULL," \
#               "structure TEXT NOT NULL," \
#               "category_id INT NOT NULL)"
#
#     cur.execute(request)
#
#     # id, user_id, date, cost, place
#     request = "CREATE TABLE IF NOT EXISTS orders(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "user_id INT NOT NULL," \
#               "date TEXT NOT NULL," \
#               "cost FLOAT NOT NULL," \
#               "address TEXT NOT NULL," \
#               "distance FLOAT NOT NULL," \
#               "user_contact TEXT NOT NULL," \
#               "data_order TEXT NOT NULL," \
#               "approx_sum FLOAT NOT NULL)"
#
#     cur.execute(request)
#
#     request = "CREATE TABLE IF NOT EXISTS packs(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "order_id INT NOT NULL," \
#               "count TEXT NOT NULL," \
#               "input TEXT NOT NULL);"
#
#     cur.execute(request)
#
#     # id, order_id, product_id, cost_product, status
#     request = "CREATE TABLE IF NOT EXISTS sold(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "order_id INT NOT NULL," \
#               "product_id INT NOT NULL," \
#               "cost_product INT NOT NULL," \
#               "count INT NOT NULL)"
#
#     cur.execute(request)
#
#     request = "CREATE TABLE IF NOT EXISTS user_asks(" \
#               "id INT PRIMARY KEY NOT NULL," \
#               "ask TEXT NOT NULL," \
#               "answer TEXT NOT NULL);"
#
#     cur.execute(request)
#
#     conn.commit()
#
#     return conn, cur
#
#
# conn, cur = sql_start()
#
#
# # id, ask, answer
# def add_user_ask(ask, answer):
#     try:
#         request = "SELECT * FROM user_asks WHERE ask = ?"
#
#         if cur.execute(request, (ask,)).fetchall():
#             return 0
#         request = "SELECT * FROM user_asks"
#         num_id = len(cur.execute(request).fetchall()) + 1
#
#         requests = "INSERT INTO user_asks VALUES (?, ?, ?);"
#         cur.execute(requests, (num_id, ask, answer))
#         conn.commit()
#         return True
#     except Exception as ex:
#         print(ex)
#         return False
#
#
# def get_user_asks():
#     request = "SELECT * FROM user_asks"
#     user_asks = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         user_asks.append(elem)
#     return user_asks
#
#
# # print(add_user_ask("ask one", "answer one"))
# # print(add_user_ask("ask two", "answer two"))
# # print(add_user_ask("ask three", "answer three"))
# # print(get_user_asks())
#
#
# # id, mail, contact, password, status
# def add_user(mail, contact, password, status="client"):
#     try:
#         request = "SELECT * FROM users WHERE contact = ?"
#
#         if cur.execute(request, (contact,)).fetchall():
#             return 0
#         request = "SELECT * FROM users"
#         num_id = len(cur.execute(request).fetchall()) + 1
#
#         requests = "INSERT INTO users VALUES (?, ?, ?, ?, ?);"
#         cur.execute(requests, (num_id, mail, contact, password, status))
#         conn.commit()
#         return True
#     except Exception as ex:
#         print(ex)
#         return False
#
#
# def add_admin(mail, contact, password):
#     status = "admin"
#     result = add_user(mail, contact, password, status=status)
#     if result:
#         return True
#     else:
#         return False
#
#
# def get_users():
#     request = "SELECT * FROM users"
#     users = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         users.append(elem)
#     return users
#
#
# # def get_user_id(user_id):
# #     request = "SELECT * FROM users WHERE "
#
#
# # print(add_user("mail", "8263488", "pass123", "base"))
# # print(add_user("mail", "898", "pass123", "base"))
# # print(add_user("mail", "888", "pass123", "base"))
# #
# #
# # add_admin("main", "777", "pass")
# # print(get_users())
#
#
# # id, title, describe, image, price, structure
# def add_category_product(title, describe):
#     try:
#
#         request = "SELECT * FROM category_product WHERE title = ?"
#
#         if cur.execute(request, (title,)).fetchall():
#             return 0
#         request = "SELECT * FROM category_product"
#         num_id = len(cur.execute(request).fetchall()) + 1
#
#         requests = "INSERT INTO category_product VALUES (?, ?, ?);"
#         cur.execute(requests, (num_id, title, describe))
#         conn.commit()
#         print("done")
#         return True
#
#     except Exception as ex:
#         print(ex)
#         return False
#
#
# def get_category():
#     request = "SELECT * FROM category_product"
#     category = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         category.append(elem)
#     return category
#
# #
# # print(add_category_product("title1", "describe"))
# # print(add_category_product("title2", "describe"))
# # print(add_category_product("title3", "describe"))
# #
# #
# # print(get_category())
#
#
# # id, title, describe, image, price, structure, category
# def add_product(title, describe, image, price, structure, category):
#     try:
#
#         request = "SELECT * FROM products WHERE title = ?"
#
#         if cur.execute(request, (title,)).fetchall():
#             return 0
#
#         request = "SELECT id FROM category_product WHERE title = ?"
#
#         if not cur.execute(request, (category,)).fetchall():
#             return 0
#
#         request = "SELECT id FROM products"
#         print(len(cur.execute(request).fetchall()))
#
#         result = cur.execute(request).fetchall()
#         if len(result) == 0:
#             num_id = 0
#         else:
#             num_id = result[-1][0] + 1
#
#         requests = "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?);"
#         cur.execute(requests, (num_id, title, describe, image, price, structure, category))
#         conn.commit()
#         print("done")
#         return True
#
#     except Exception as ex:
#         print(ex)
#         return False
#
#
# def del_product(product_title):
#     try:
#         request = "DELETE FROM products WHERE title = ?;"
#         cur.execute(request, (product_title,))
#         conn.commit()
#         request = "SELECT * FROM products WHERE title = ?;"
#         result = cur.execute(request, (product_title,)).fetchall()
#         if result:
#             return "Запись не удалена"
#         else:
#             return "Запись успешно удалена"
#     except Exception as ex:
#         print(ex)
#         return "Произошла ошибка"
#
#
# def get_products():
#     request = "SELECT * FROM products"
#     products = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         products.append(elem)
#     return products
#
#
# def get_product_title(product_title):
#     request = "SELECT * FROM products WHERE title = ?;"
#     product = cur.execute(request, (product_title,)).fetchall()
#     return product
#
#
# def get_product_id(product_id):
#     request = "SELECT title FROM products WHERE id = ?;"
#     product = cur.execute(request, (product_id,)).fetchall()[0]
#     return product
#
#
# # print(add_product("title1", "describe",
# # "AgACAgIAAxkBAAIFj2Nhf5sYSrW5BZbA8KnrhukvbrudAAKEwjEbLzgJS5q8nU_0xg4dAQADAgADcwADKgQ", 100, "structure", "title1"))
# # print(add_product("title2", "describe",
# # "AgACAgIAAxkBAAIFj2Nhf5sYSrW5BZbA8KnrhukvbrudAAKEwjEbLzgJS5q8nU_0xg4dAQADAgADcwADKgQ", 200, "structure", "title1"))
# # print(add_product("title3", "describe",
# # "AgACAgIAAxkBAAIFj2Nhf5sYSrW5BZbA8KnrhukvbrudAAKEwjEbLzgJS5q8nU_0xg4dAQADAgADcwADKgQ", 250, "structure", "title1"))
#
# # #
# # print(get_products())
# # print(del_product("title3"))
# # print(get_products())
#
# #
# # print(get_product_title("title1"))
#
#
# def add_sold(order_id, elem, product_title):
#     request = "SELECT * FROM sold"
#     num_id = len(cur.execute(request).fetchall()) + 1
#
#     cost = elem["cost"]
#     count = elem["count"]
#
#     request = "SELECT id FROM products WHERE title = ?;"
#     id_product = cur.execute(request, (product_title,)).fetchall()[0][0]
#     print(id_product)
#
#     requests = "INSERT INTO sold VALUES (?, ?, ?, ?, ?);"
#     cur.execute(requests, (num_id, order_id, id_product, cost, count))
#     conn.commit()
#
#
# def get_sold():
#     request = "SELECT * FROM sold"
#     sold = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         sold.append(elem)
#     return sold
#
#
# def get_sold_order_id(order_id):
#     request = "SELECT * FROM sold WHERE order_id = ?"
#     sold = list()
#     for elem in cur.execute(request, (order_id,)).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         sold.append(elem)
#     return sold
#
#
# def add_pack_input(packs, order_id):
#     request = "SELECT * FROM packs"
#     num_id = len(cur.execute(request).fetchall()) + 1
#
#     for elem in packs:
#         pack_title = elem
#         for inp in packs[elem]:
#             product_input = ", ".join(inp)
#             request = "INSERT INTO packs VALUES (?, ?, ?, ?);"
#             cur.execute(request, (num_id, order_id, pack_title, product_input))
#             num_id += 1
#
#     conn.commit()
#
#
# def get_packs_order_id(order_id):
#     packs = list()
#
#     request = "SELECT * FROM packs WHERE order_id = ?;"
#
#     for elem in cur.execute(request, (order_id,)).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         packs.append(elem)
#     return packs
#
#
# def get_packs():
#     packs = list()
#
#     request = "SELECT * FROM packs;"
#
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         packs.append(elem)
#     return packs
#
#
# basket = {
#     "title1": {
#         "cost": 100,
#         "count": 2
#     },
#     "title2": {
#         "cost": 1003,
#         "count": 1
#     },
#     "title3": {
#         "cost": 1030,
#         "count": 5
#     },
#
# }
#
# # print(add_sold(1, basket[0]))
# # print(add_sold(2, basket[0]))
# # print(add_sold(5, basket[0]))
# #
# #
# # print(get_sold())
#
#
# # id, user_id, date, cost, place
# def add_orders(id_users, basket, date, place, distance, contact, data_order, approx_sum, packs):
#
#     # basket : [{"id": id, "price": price}]
#     request = "SELECT * FROM orders"
#     num_id = len(cur.execute(request).fetchall()) + 1
#
#     cost = 0
#
#     for elem in basket:
#         cost += basket[elem]["count"] * basket[elem]["cost"]
#         add_sold(num_id, basket[elem], elem)
#
#     add_pack_input(packs, num_id)
#
#     requests = "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
#     cur.execute(requests, (num_id, id_users, date, cost, place, distance, contact, data_order, approx_sum))
#     conn.commit()
#     print("done")
#
#
# def get_orders():
#     request = "SELECT * FROM orders"
#     orders = list()
#     for elem in cur.execute(request).fetchall():
#         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
#         orders.append(elem)
#     return orders
#
#
# # add_orders(777, basket, 000, "Moscow", 12, "8999999999", '12.23.2023', 23412)
# # add_orders(777, basket, 000, "Moscow", 13, "8999999999", '12.23.2023', 1234)
# # add_orders(777, basket, 000, "Moscow", 15, "8999999999", '12.23.2023', 2314)
# #
# #
# # print(get_orders())
#
# #
# # # id, order_id, product_id, cost_product, status
# # def add_sold(id_orders, id_product, cost):
# #     request = "SELECT * FROM sold"
# #     num_id = len(cur.execute(request).fetchall()) + 1
# #
# #     requests = "INSERT INTO sold VALUES (?, ?, ?, ?);"
# #     cur.execute(requests, (num_id, id_orders, id_product, cost))
# #     conn.commit()
# #     print("done")
# #
# #
#
#
# def get_user(mail):
#     requests = "SELECT * FROM users WHERE mail = ?"
#     result = cur.execute(requests, (mail,)).fetchall()
#     if result:
#         return [True, result[0]]
#     else:
#         return [False]
#
#
# # def get_products():
# #     requests = "SELECT * FROM products"
# #     result = cur.execute(requests).fetchall()
# #     if result:
# #         return [True, result]
# #     else:
# #         return [False]
#
# # print(get_user("test_three@mail.com")[1][2])
# # add_user("test_three@mail.com", "812343241", "qwerty321123")
#
#
# def sql_add(login, password):
#     request = "INSERT INTO users VALUES ('login', 'password')"
#     cur.execute(request, ("test_one", "qwerty1"))
#     conn.commit()
#     print("done")
#
#
# # def show_users():
# #     request = "SELECT * FROM users"
# #     users = list()
# #     for elem in cur.execute(request).fetchall():
# #         # print(f"ID: {elem[0]},\nLogin: {elem[1]},\nPassword: {elem[2]}")
# #         users.append(elem)
# #     return users
#
# # sql_add("some_login_one", "password_1")
# # sql_add("some_login_two", "password_2")
# # sql_add("some_login_three", "password_3")
# #
#
#
# # add_admin("test_mail@gmail.com", "+79528370781", "passwordHard")
#
# # print(show_users())
