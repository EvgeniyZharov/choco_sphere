from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_keyboards(btn_list, cancel_btn=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for elem in btn_list:
        kb.add(KeyboardButton(elem))
    if cancel_btn:
        kb.add(KeyboardButton("Отмена"))

    return kb


def start_admin():

    # btn_list = ["Добавить товар",
    #             "Удалить товар",
    #             "Посмотреть заказы",
    #             "Посмотреть статистику",
    #             "Посмотреть товар",
    #             "Добавить категорию",
    #             "Добавить вопрос-ответ"]
    btn_list = [
        "Посмотреть товар",
        "Посмотреть заказы",
        "Посмотреть тикеты клиентов",
        "Частые вопросы",
        "Посмотреть аналитику",
        "Настройки"
    ]

    kb = create_keyboards(btn_list)

    return kb


def acception_btn():
    btn_list = [
        "Да"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_btn():
    btn_list = [
        "Категории",
        "Продукты",
        "Вопрос-ответ",
        "Аккаунт",
        "Добавить нового администратора"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_category_btn():
    btn_list = [
        "Создать",
        # "Изменить",
        "Удалить"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_product_btn():
    btn_list = [
        "Создать",
        # "Изменить",
        "Удалить"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_product_category_btn(category_btn):
    kb = create_keyboards(category_btn, cancel_btn=True)

    return kb


def settings_ask_answer_btn():
    btn_list = [
        "Создать",
        # "Изменить",
        "Удалить"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_add_admin_btn():
    btn_list = [
        "Создать ключ",
        # "Ввести ключ другой стороны",
        "Удалить все ключи"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def settings_account_btn():
    btn_list = [
        "Изменить номер",
        "Изменить пароль"
    ]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


def get_ticket_btn():

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text="<", callback_data="-"),
           InlineKeyboardButton(text=">", callback_data="+"))
    kb.add(InlineKeyboardButton(text="Написать", callback_data="answer"),
           InlineKeyboardButton(text="Изменить статус", callback_data="change_status"))

    return kb


def get_order_btn():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text="<", callback_data="-"),
           InlineKeyboardButton(text=">", callback_data="+"))
    kb.add(InlineKeyboardButton(text="Написать", callback_data="answer"),
           InlineKeyboardButton(text="Изменить статус", callback_data="change_status"))

    return kb


def get_some_list_btn(some_list):

    kb = create_keyboards(some_list, cancel_btn=True)

    return kb


def get_type_ticket_order_status_btn():
    btn_list = ["Актуальные", "Все"]

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text=btn_list[0], callback_data="status actual"),
           InlineKeyboardButton(text=btn_list[1], callback_data="status all"))

    return kb


def get_analityc_btn():
    btn_list = ["Количество заказанных",
                "Общая стоимость заказанных"]

    kb = create_keyboards(btn_list, cancel_btn=True)

    return kb


# def accept():
#     btn_list = [
#         "Подтвердить",
#     ]
#
#     kb = create_keyboards(btn_list, cancel_btn=True)
#
#     return kb


#
# def get_del_product_btn(product_title):
#     kb = InlineKeyboardMarkup(row_width=2)
#     kb.add(InlineKeyboardButton(text="<", callback_data="-"),
#            InlineKeyboardButton(text=">", callback_data="+"))
#     kb.add(InlineKeyboardButton(text="Удалить", callback_data=f"del {product_title}"))
#
#     return kb
#
#
# def get_category_product_btn(btn_list):
#     kb = create_keyboards(btn_list, cancel_btn=True)
#     return kb
#
