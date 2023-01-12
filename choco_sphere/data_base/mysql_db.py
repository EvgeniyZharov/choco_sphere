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

def contact():
    global con
    try:
        con = pymysql.Connection(
                host=host,
                user=user,
                port=3306,
                password=password,
                use_unicode=True,
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
        return True
    except Exception:
        return False


def connecting():
    global con
    try:
        con = pymysql.Connection(
            host=host,
            user=user,
            port=3306,
            password=password,
            use_unicode=True,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
#         con.set_charset('utf8')
#         with con.cursor() as cur:
#             cur.execute('SET NAMES utf8;')
#             cur.execute('SET CHARACTER SET utf8;')
#             cur.execute('SET character_set_connection=utf8;')
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
                                 category_title VARCHAR(100),
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

def add_users_in_table(user_id, phone, user_password, user_status="client"):
    try:
        request = """INSERT INTO db_chocosphere.users (user_id, phone, user_password, user_status) VALUES (%s, %s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(user_id, phone, user_password, user_status)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

        return True
    except Exception:
        return False


def add_admin_in_table(user_id, phone, user_password):
    result = add_users_in_table(user_id, phone, user_password, user_status="admin")
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


def add_sold_pack_in_table(order_id, product_title, category_title, count, one_price):
    try:
        request = """INSERT INTO db_chocosphere.sold_pack (order_id, product_title, category_title, count, one_price) VALUES (%s, %s, %s, %s, %s);"""
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(order_id, product_title, category_title, count, one_price)]
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
        request = f"SELECT * FROM db_chocosphere.{table_title}"
        with con.cursor() as cur:
            cur.execute(request)
        elem_list = cur.fetchall()
        # if len(elem_list) > 0:
        return elem_list
        # else:
        #     connecting()
        #     return get_table(table_title)


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
            elem_list = cur.fetchall()
            # if len(elem_list) > 0:
            return [True, elem_list]
            # else:
            #     connecting()
            #     return get_elements_table(table_title, elements)
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
            elem_list = cur.fetchall()
            # if len(elem_list) > 0:
            return [True, elem_list]
            # else:
            #     connecting()
            #     return get_elem_for_elem(table_title, elements, condition_1, condition_2)
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
    result = get_elem_for_elem(TABLES[4], ['product_title', 'category_title', 'count', 'one_price'], "order_id", order_id)
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

def add_new_solds_packs(basket, order_id):
    try:
        for category_title in basket:
            for product_title in basket[category_title]:
                count = basket[category_title][product_title]["count"]
                price = basket[category_title][product_title]["price"]
                add_sold_pack_in_table(order_id, product_title, category_title, count, price)
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
print(add_admin_in_table("404248385", "+79999999999", "pass"))
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
