import matplotlib.pyplot as plt
from data_base.mysql_db import get_sold_pack_table
import os

#
# def del_file(name):
#     if os.path.isfile(name):
#         os.remove(name)
#         print("DEL")
#     else:
#         print("not DEL")


def get_histogram(file_name, type_histogram=1):

    sold_list = get_sold_pack_table()

    plt.close()

    if type_histogram == 1:
        count_dict = dict()
        for elem in sold_list:
            if elem["product_title"] in count_dict:
                count_dict[elem['product_title']] += elem["count"]
            else:
                count_dict[elem['product_title']] = elem["count"]
        data_a = list(count_dict.keys())
        data_b = list(count_dict.values())
        plt.xlabel("Продукт")
        plt.ylabel("Количество")

    elif type_histogram == 2:
        price_dict = dict()
        for elem in sold_list:
            if elem["product_title"] in price_dict:
                price_dict[elem['product_title']] += elem["count"] * elem["one_price"]
            else:
                price_dict[elem['product_title']] = elem["count"] * elem["one_price"]
            data_a = list(price_dict.keys())
            data_b = list(price_dict.values())
            plt.xlabel("Продукт")
            plt.ylabel("Общая стоимость")

    elif type_histogram == 3:
        category_dict = dict()
        for elem in sold_list:
            if elem["category_title"] in category_dict:
                category_dict[elem['category_title']] += elem["count"]
            else:
                category_dict[elem['category_title']] = elem["count"]
            data_a = list(category_dict.keys())
            data_b = list(category_dict.values())
            plt.xlabel("Категория")
            plt.ylabel("Общая стоимость")

    #
    #
    #
    # products = get_products()
    # product_list = dict()
    # for elem in products:
    #     prod_id = elem[0]
    #     prod_title = elem[1]
    #     product_list[prod_id] = prod_title
    # sold = get_sold()
    # # print(sold)
    # for elem in sold:
    #     data_dict[product_list[elem[2]]] = elem[4]
    # data_a = list(data_dict.keys())
    plt.bar(data_a, data_b)
    plt.title("Аналитика!")

    plt.savefig(file_name)


# get_histogram("test_1", type_histogram=2)
# get_histogram("test_1", type_histogram=1)
#
