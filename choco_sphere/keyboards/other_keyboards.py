from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar


def create_keyboards(btn_list, cancel_btn=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for elem in btn_list:
        kb.add(KeyboardButton(elem))

    if cancel_btn:
        kb.add(KeyboardButton("Отмена"))

    return kb


def start_keyboards():

    btn_list = ["Посмотреть товар",
                "Собрать подарок",
                # "Посмотреть отложенное",
                "Частые вопросы",
                "Задать вопрос"]
    kb_start = create_keyboards(btn_list, cancel_btn=False)

    return kb_start


def set_contact_user():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Отправить контакт", request_contact=True))
    kb.add(KeyboardButton("Назад"))
    kb.add(KeyboardButton("Отмена"))

    return kb


def set_location_user():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Отправить местоположение", request_location=True))
    kb.add(KeyboardButton("Назад"))
    kb.add(KeyboardButton("Отмена"))

    return kb


def get_category_btn(to_box=False):

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text="<", callback_data="-"),
           InlineKeyboardButton(text=">", callback_data="+"))
    kb.add(InlineKeyboardButton(text="Описание", callback_data="info"))
    kb.add(InlineKeyboardButton(text="Выбрать", callback_data="choice"))
    if to_box:
        kb.add(InlineKeyboardButton(text="Назад", callback_data="back"))

    return kb


def choice_type_delivery_btn():
    btn_list = ["Доставка",
                "Самовывоз",
                "Назад"]
    kb_start = create_keyboards(btn_list, cancel_btn=True)

    return kb_start


def get_calendar_years(start_year):
    actual_year = datetime.datetime.today().year
    if start_year < actual_year:
        start_year = actual_year

    year_list = [ii for ii in range(start_year, start_year + 5)]
    kb = InlineKeyboardMarkup(row_width=5)

    kb.add(InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="<", callback_data=f"-"),
           InlineKeyboardButton(text="Год", callback_data=f"ignore"),
           InlineKeyboardButton(text=">", callback_data=f"+"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           )

    kb.add(InlineKeyboardButton(text=f"{year_list[0]}", callback_data=f"year {year_list[0]}"),
           InlineKeyboardButton(text=f"{year_list[1]}", callback_data=f"year {year_list[1]}"),
           InlineKeyboardButton(text=f"{year_list[2]}", callback_data=f"year {year_list[2]}"),
           InlineKeyboardButton(text=f"{year_list[3]}", callback_data=f"year {year_list[3]}"),
           InlineKeyboardButton(text=f"{year_list[4]}", callback_data=f"year {year_list[4]}"),
           )

    kb.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back"))

    return kb


def get_calendar_month(year):
    mount_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    kb = InlineKeyboardMarkup(row_width=6)

    kb.add(InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="<", callback_data=f"-"),
           InlineKeyboardButton(text=f"{year}", callback_data=f"back_to_year"),
           InlineKeyboardButton(text=">", callback_data=f"+"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           )

    for elem in mount_list:
        kb.insert(InlineKeyboardButton(text=elem, callback_data=f"month {mount_list.index(elem)}"))

    return kb


def get_calendar_day(year, month):
    first_day = datetime.datetime(year, month, 1)
    blank_days = first_day.isoweekday() - 2

    mount_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    day_title = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    print(year, month)
    count_day = calendar.monthrange(year, month)[1]
    print(blank_days, count_day)

    kb = InlineKeyboardMarkup(row_width=7)

    kb.add(InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text=f"{year}", callback_data=f"back_to_year"),
           InlineKeyboardButton(text=f"{mount_list[month - 1]}", callback_data=f"back_to_month"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           InlineKeyboardButton(text="", callback_data=f"ignore"),
           )

    for elem in day_title:
        kb.insert(InlineKeyboardButton(text=f"{elem}", callback_data=f"ignore"))

    week_ticket = 0

    for ii in range(-blank_days, count_day + 1):
        week_ticket += 1
        if ii <= 0:
            kb.insert(InlineKeyboardButton(text=" ", callback_data=f"ignore"))
            continue
        kb.insert(InlineKeyboardButton(text=f"{ii}", callback_data=f"day {ii}"))
        if week_ticket == 7:
            week_ticket = 0

    while week_ticket != 7 and week_ticket != 0:
        kb.insert(InlineKeyboardButton(text=f" ", callback_data=f"ignore"))
        week_ticket += 1

    return kb


def get_for_comment_btn():
    kb = create_keyboards(["Завершить заказ"], cancel_btn=True)
    return kb


def get_user_asks(asks_list):
    kb = create_keyboards(asks_list, cancel_btn=True)

    return kb


# def get_category_btn(list_btn):
#     kb = create_keyboards(list_btn, cancel_btn=True)
#
#     return kb


# def choice_product():
#     kb = create_keyboards(["Перейти к выбору упаковки"], cancel_btn=True)
#
#     return kb


# def choice_yes_no():
#     kb = InlineKeyboardMarkup(row_width=2)
#     kb.add(InlineKeyboardButton(text="Да", callback_data="+"),
#            InlineKeyboardButton(text="Нет", callback_data="-"))
#
#     return kb


# def choice_packet_num():
#     kb = InlineKeyboardMarkup(row_width=2)
#     kb.add(InlineKeyboardButton(text="1", callback_data="1"),
#            InlineKeyboardButton(text="2", callback_data="2"))
#     kb.add(InlineKeyboardButton(text="3", callback_data="3"),
#            InlineKeyboardButton(text="4", callback_data="4"))
#     # kb.add(InlineKeyboardButton(text="Сбросить", callback_data="-"))
#
#     return kb


def get_product_btn(to_box=False, full=False):
    kb = InlineKeyboardMarkup(row_width=2)
    if full:
        kb.add(InlineKeyboardButton(text="Продолжить", callback_data="continue"))
    kb.add(InlineKeyboardButton(text="<", callback_data="-"),
           InlineKeyboardButton(text=">", callback_data="+"))
    kb.add(InlineKeyboardButton(text="Состав", callback_data="info_1"),
           InlineKeyboardButton(text="Описание", callback_data="info_2"))
    if to_box:
        kb.add(InlineKeyboardButton(text="Добавить", callback_data="add"),
               InlineKeyboardButton(text="Удалить", callback_data="delete"))
    kb.add(InlineKeyboardButton(text="Назад", callback_data="back"))

    return kb


def choice_count_places_in_boxes():
    btn_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    kb = InlineKeyboardMarkup(row_width=2)

    for ii in range(len(btn_list) // 2):
        kb.add(InlineKeyboardButton(text=btn_list[ii*2], callback_data=f"count_pack {btn_list[ii*2]}"),
               InlineKeyboardButton(text=btn_list[ii*2 + 1], callback_data=f"count_pack {btn_list[ii*2 + 1]}"))

        # kb.row(KeyboardButton(btn_list[ii*2]), KeyboardButton(btn_list[ii*2 + 1]))

    # kb.add(InlineKeyboardButton(text="Отмена", callback_data=f"cancel_one"))

    return kb

