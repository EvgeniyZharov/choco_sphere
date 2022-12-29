from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def create_keyboards(btn_list, cancel_btn=False):
    kb = ReplyKeyboardMarkup()
    for elem in btn_list:
        kb.add(KeyboardButton(elem))

    if cancel_btn:
        kb.add(KeyboardButton("Отмена"))

    return kb


def start_keyboards():

    btn_list = ["Посмотреть товар",
                "Собрать подарки",
                # "Посмотреть отложенное",
                "Частые вопросы",
                "Задать вопрос"]
    kb_start = create_keyboards(btn_list, cancel_btn=False)

    return kb_start


def set_contact_user():
    kb = ReplyKeyboardMarkup()
    kb.add(KeyboardButton("Отправить контакт", request_contact=True))

    return kb
