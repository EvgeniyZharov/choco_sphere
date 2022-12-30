from aiogram import types, Dispatcher
from start_bot import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_keyboards, admin_keyboards, other_keyboards
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from add_function import find_distance

from data_base import get_users_table
from data_base import get_from_phone_user
from data_base import get_category_table
from data_base import get_list_category
from data_base import get_from_category_product
from data_base import get_product_table
from data_base import add_orders_in_table
from data_base import get_orders_table
from data_base import add_new_solds_packs
from data_base import get_ask_answer_table
from data_base import get_list_ask
from data_base import get_from_ask_answer
from data_base import add_user_ticket_in_table
from data_base import add_admin_in_table


import datetime


# from data_base import add_user, get_users, get_user, add_admin, get_products
# from data_base import add_admin, get_user_asks, get_products, get_category
# from data_base import add_orders, get_orders

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# from add_function import find_distance, find_sum

# from datetime import datetime

# from data_base import get_orders
# from data_base import get_sold_order_id


asks_dict = dict()

INT_PLACE = 0

ADMINS = ["961023982"]
ADD_ADMIN_KEYS = list()
ADD_ADMIN_KEY = "not"
ACCOUNTS = dict()


class FSMReg(StatesGroup):
    mail = State()
    phone = State()
    password = State()


class FSMShowProduct(StatesGroup):
    choice_category_product = State()
    choice_product = State()
    # choice_type_pack = State()
    # choice_pack = State()
    # choice_address = State()
    # choice_date = State()
    # check_user_status = State()
    # get_user_contact = State()
    # get_comment = State()
    # accept = State()


class FSMSetBox(StatesGroup):
    # choice_count_of_box = State()
    start_set_box = State()
    choice_count_in_box = State()
    choice_category = State()
    choice_product = State()
    choice_type_delivery = State()
    # choice_type_choice = State()
    choice_address = State()
    set_year = State()
    set_mount = State()
    set_day = State()
    get_user_contact = State()
    get_comment = State()
    # accept = State()


class FSMUserAsks(StatesGroup):
    status = State()


class FSMSetTicket(StatesGroup):
    status = State()


class FSMAuthorization(StatesGroup):
    phone = State()
    password = State()


class FSMAddAdmin(StatesGroup):
    add_new_admin = State()
    input_key = State()
    input_contact = State()
    input_password = State()


def get_text_for_client_check(data):
    basket = data["basket"]
    basket_price = data["basket_price"]
    location = data["location"]
    if location["type"] == "self":
        distance = 0
        distance_text = "Доставка: 0 (самовывоз)"
    elif location["type"] == "button":
        distance = find_distance(f"{location['latitude']} - {location['longitude']}", type_place=2)
        price_2 = float(str(distance).split()[0]) * 100
        distance_text = f"Стоимость доставки: {price_2}"
    else:
        distance = find_distance(location["address"])
        price_2 = float(str(distance).split()[0]) * 100
        distance_text = f"Стоимость доставки: {price_2}"

    date = f"{data['day_order']}.{data['month_order']}.{data['year_order']}"

    contact = data["contact"]

    basket_text = "\nКорзина:\n"
    all_price = 0
    for elem in basket:
        basket_text += f"{elem}\nКоличество: {basket[elem]}\nЦена: {basket_price[elem]}\n"
        all_price += basket[elem] * basket_price[elem]

    text = f"Ваш заказ на {date}\nВаш контакт: {contact}" \
           f"\n{basket_text}\nСтоимость за сладости: {all_price}\n"

    text += distance_text

    return text


test_command = ['test']


@dp.message_handler(commands=test_command)
async def input_add_admin_key(msg: types.Message):
    await msg.answer(msg.from_user.id)


@dp.message_handler(commands=["add_admin"])
async def input_add_admin_key(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        return

    await msg.answer("Введите ключ для создания аккаунта админа",
                     reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
    await FSMAddAdmin.add_new_admin.set()


@dp.message_handler(state=FSMAddAdmin.add_new_admin)
async def input_add_admin_key(msg: types.Message):
    if msg.text in ADD_ADMIN_KEYS:
        await msg.answer("Нужно ввести Ваш номер, для этого нажмите на кнопку",
                         reply_markup=other_keyboards.set_contact_user(back_btn=False))
        await FSMAddAdmin.input_key.set()


@dp.message_handler(content_types=["contact"], state=FSMAddAdmin.input_key)
async def func(msg: types.Message, state: FSMContext):
    contact = msg["contact"]["phone_number"]
    async with state.proxy() as data:
        data["contact"] = str(contact)
    await msg.answer("Теперь введите пароль для Вашего аккаунта",
                     reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
    await FSMAddAdmin.input_contact.set()


@dp.message_handler(state=FSMAddAdmin.input_contact)
async def func(msg: types.Message, state: FSMContext):
    password = str(msg.text)
    user_id = str(msg.from_user.id)
    async with state.proxy() as data:
        contact = str(data["contact"])
    result = add_admin_in_table(user_id, contact, password)
    if result:
        ADMINS.append(user_id)
        ADD_ADMIN_KEYS.clear()
        await msg.answer("Ваш аккаунт успешно создан. Теперь Вам доступны настройки админа",
                         reply_markup=admin_keyboards.start_admin())
    else:
        await msg.answer("Произошла ошибка",
                         reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
    await FSMAddAdmin.input_password.set()


# CANCEL

@dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
async def cancel(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await bot.send_message(msg.from_user.id, "Вы вернулись в главное меню, Админ!",
                               reply_markup=admin_keyboards.start_admin())
    else:
        await bot.send_message(msg.from_user.id, "Вы вернулись в главное меню",
                               reply_markup=other_keyboards.start_keyboards())


# START

@dp.message_handler(commands=["start"], state="*")
async def start(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:

        await bot.send_message(msg.from_user.id, "Добро пожаловать, Админ!",
                               reply_markup=admin_keyboards.start_admin())
    else:
        await bot.send_message(msg.from_user.id, "Добро пожаловать!",
                               reply_markup=other_keyboards.start_keyboards())


# LOG IN ADMIN ACCOUNT

@dp.message_handler(commands=["log_in"], state="*")
async def log_in(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Вы уже авторизированы.")
        return
    current_state = await state.get_state()
    if current_state:
        await state.finish()

    await msg.reply("Введите свой телефон.", reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

    await FSMAuthorization.phone.set()


## INPUT PHONE FOR ACCOUNT

@dp.message_handler(state=FSMAuthorization.phone)
async def authorization_phone(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = get_from_phone_user(msg.text)
        if user:
            data["user"] = user
            print(user)

            await msg.answer("Введите свой пароль: ")

            await FSMAuthorization.next()
        else:
            await msg.answer("Аккаунта с таким телефонным номером не найдено.")
    await msg.delete()


## INPUT PASSWORD FOR ACCOUNT

@dp.message_handler(state=FSMAuthorization.password)
async def authorization_password(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        user = data["user"]
        if msg.text == user["user_password"]:
            user_id = str(msg.from_user.id)
            # await msg.answer("Добропожаловать! Вы вошли в свой аккаунт.",
            #                  reply_markup=client_keyboards.start_keyboards())
            # ACCOUNTS[user_id] = "client"

            if user["user_status"] == "admin":
                await msg.answer("Аккаунт администратора запущен.", reply_markup=admin_keyboards.start_admin())
                ADMINS.append(user_id)
            await state.finish()
        else:
            await msg.answer("Некорректно введен пароль.")

    await msg.delete()


# LOG OUT FROM ADMIN ACCOUNT

@dp.message_handler(commands=["log_out"], state="*")
async def log_out(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        current_state = await state.get_state()
        if current_state:
            await state.finish()
        ADMINS.remove(str(msg.from_user.id))
        await msg.reply("Закрываем режим Админа", reply_markup=other_keyboards.start_keyboards())


# SHOW ALL PRODUCT CHOICE CATEGORY

@dp.message_handler(Text(equals="Посмотреть товар", ignore_case=True))
async def show_product(msg: types.Message, state: FSMContext):

    category_list = get_category_table()  # NEED UPDATES (TAKE ALL LINES, BUT USING ONLY ONE)
    if category_list:
        async with state.proxy() as data:

            data["category_index"] = 0
            data["category_start_index"] = 0
            data["category_end_index"] = len(category_list) - 1

            category = category_list[data["category_index"]]
            data["category"] = category

            text = f"{category['title']}"

            await msg.answer("Веберите категорию",
                             reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

            msg = await msg.answer_photo(category['image_link'], text,
                                         reply_markup=other_keyboards.get_category_btn())

            data["msg_link"] = msg["message_id"]

            await FSMShowProduct.choice_category_product.set()
    else:
        await msg.answer("Пока ничего нет")


## SHOW PREVIOUS CATEGORY

@dp.callback_query_handler(text="-", state=FSMShowProduct.choice_category_product)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["category_index"] - 1 < data["category_start_index"]:
            await callback.answer("Это самое начало")
            return
        data["category_index"] -= 1
        category = get_category_table()[data["category_index"]]
        data["category"] = category

        text = f"{category['title']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn())

        data["msg_link"] = msg["message_id"]


## SHOW NEXT CATEGORY

@dp.callback_query_handler(text="+", state=FSMShowProduct.choice_category_product)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["category_index"] + 1 > data["category_end_index"]:
            await callback.answer("Это был последний")
            return
        data["category_index"] += 1
        category = get_category_table()[data["category_index"]]
        data["category"] = category

        text = f"{category['title']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn())

        data["msg_link"] = msg["message_id"]


## SHOW INFO ABOUT CATEGORY

@dp.callback_query_handler(text="info", state=FSMShowProduct.choice_category_product)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data["category"]

        category_info = f"Описание: {category['category_description']}"

    await callback.answer(category_info, show_alert=True)


## SHOW PRODUCT IN THE CATEGORY

@dp.callback_query_handler(text="choice", state=FSMShowProduct.choice_category_product)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data["category"]

        category_id = category["category_id"]

        product_list = get_from_category_product(category_id)
        if product_list:

            data["product_index"] = 0
            data["product_start_index"] = 0
            data["product_end_index"] = len(product_list) - 1
            product = product_list[data["product_index"]]
            data["product"] = product

            await callback.answer()

            text = f"{product['title']}\nЦена: {product['price']}"

            await bot.delete_message(callback.from_user.id, callback.message.message_id)

            msg = await callback.message.answer_photo(product['image_link'], text,
                                                      reply_markup=other_keyboards.get_product_btn())

            data["msg_link"] = msg["message_id"]

            await FSMShowProduct.next()
        else:
            await callback.answer("Здесь пока ничего нет")
            return


## SHOW PREVIOUS PRODUCT

@dp.callback_query_handler(text="-", state=FSMShowProduct.choice_product)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["product_index"] - 1 < data["product_start_index"]:
            await callback.answer("Это самое начало")
            return
        category_id = data["category"]["category_id"]
        data["product_index"] -= 1
        # product = get_product_table()[data["product_index"]]
        product = get_from_category_product(category_id)[data["product_index"]]
        data["product"] = product

        text = f"{product['title']}\nЦена: {product['price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn())

        data["msg_link"] = msg["message_id"]


## SHOW PREVIOUS PRODUCT

@dp.callback_query_handler(text="+", state=FSMShowProduct.choice_product)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["product_index"] + 1 > data["product_end_index"]:
            await callback.answer("Это был последний")
            return
        category_id = data["category"]["category_id"]
        data["product_index"] += 1
        # product = get_product_table()[data["product_index"]]
        product = get_from_category_product(category_id)[data["product_index"]]
        data["product"] = product

        text = f"{product['title']}\nЦена: {product['price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                                      reply_markup=other_keyboards.get_product_btn())

        data["msg_link"] = msg["message_id"]


## SHOW STRUCTURE OF THE PRODUCT

@dp.callback_query_handler(text="info_1", state=FSMShowProduct.choice_product)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = data["product"]

        product_info = f"Состав: {product['structure']}"

    await callback.answer(product_info, show_alert=True)


## SHOW INFO ABOUT PRODUCT

@dp.callback_query_handler(text="info_2", state=FSMShowProduct.choice_product)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = data["product"]

        product_info = f"Описание: {product['product_description']}"

    await callback.answer(product_info, show_alert=True)


## RETURN TO CHOICE CATEGORY

@dp.callback_query_handler(text="back", state=FSMShowProduct.choice_product)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        category = data["category"]

        text = f"{category['title']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn())

        data["msg_link"] = msg["message_id"]

        await FSMShowProduct.previous()


# START TO SET BOX

@dp.message_handler(Text(equals="Собрать подарок", ignore_case=True))
async def start_to_set_box(msg: types.Message, state: FSMContext):

    await msg.answer("Давайте соберем подарок",
                     reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

    await msg.answer("Выберите сколько сладостей хотите пололжить в коробку",
                     reply_markup=other_keyboards.choice_count_places_in_boxes())

    await FSMSetBox.start_set_box.set()


@dp.callback_query_handler(Text(startswith="count_pack"), state=FSMSetBox.start_set_box)
async def choice_count_pack(callback: types.CallbackQuery, state: FSMContext):
    try:
        count = int(callback.data.split()[1])
        async with state.proxy() as data:
            data["count_pack"] = count
            category_list = get_category_table()  # NEED UPDATES (TAKE ALL LINES, BUT USING ONLY ONE)
            if category_list:
                data["category_index"] = 0
                data["category_start_index"] = 0
                data["category_end_index"] = len(category_list) - 1

                data["count_is_set"] = 0
                data["basket"] = dict()
                data["basket_price"] = dict()

                category = category_list[data["category_index"]]
                data["category"] = category

                text = f"{category['title']}\n"

                if data["count_is_set"] > 0:
                    text += f"\n\nВаша корзина:"
                    for elem in data["basket"]:
                        text += f"\n{elem} - {data['basket'][elem]}шт."

                await bot.delete_message(callback.from_user.id, callback.message.message_id)

                await callback.message.answer("Веберите категорию",
                                              reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

                msg = await callback.message.answer_photo(category['image_link'], text,
                                                          reply_markup=other_keyboards.get_category_btn(to_box=True))

                data["msg_link"] = msg["message_id"]

                await FSMSetBox.choice_count_in_box.set()
            else:
                await callback.message.answer("Пока ничего нет")
    except Exception:
        await callback.message.answer("Нужно ввести число")


## SHOW PREVIOUS CATEGORY

@dp.callback_query_handler(text="-", state=FSMSetBox.choice_count_in_box)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["category_index"] - 1 < data["category_start_index"]:
            await callback.answer("Это самое начало")
            return
        data["category_index"] -= 1
        category = get_category_table()[data["category_index"]]
        data["category"] = category

        text = f"{category['title']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn(to_box=True))

        data["msg_link"] = msg["message_id"]


## SHOW NEXT CATEGORY

@dp.callback_query_handler(text="+", state=FSMSetBox.choice_count_in_box)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["category_index"] + 1 > data["category_end_index"]:
            await callback.answer("Это был последний")
            return
        data["category_index"] += 1
        category = get_category_table()[data["category_index"]]
        data["category"] = category

        text = f"{category['title']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn(to_box=True))

        data["msg_link"] = msg["message_id"]


## SHOW INFO ABOUT CATEGORY

@dp.callback_query_handler(text="info", state=FSMSetBox.choice_count_in_box)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data["category"]

        category_info = f"Описание: {category['category_description']}"

    await callback.answer(category_info, show_alert=True)


## SHOW PRODUCT IN THE CATEGORY

@dp.callback_query_handler(text="choice", state=FSMSetBox.choice_count_in_box)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data["category"]

        category_id = category["category_id"]

        product_list = get_from_category_product(category_id)
        if product_list:

            data["product_basket"] = {category["title"]: {}}

            data["product_index"] = 0
            data["product_start_index"] = 0
            data["product_end_index"] = len(product_list) - 1
            if "all_price" not in data:
                data["all_price"] = 0

            product = product_list[data["product_index"]]
            data["product"] = product

            await callback.answer()

            text = f"{product['title']}\nЦена: {product['price']}"

            if data["count_is_set"] > 0:
                text += f"\n\nВаша корзина:"
                for elem in data["basket"]:
                    text += f"\n{elem} - {data['basket'][elem]}шт."

            text += f"\n\nОбщая сумма: {data['all_price']}"

            await bot.delete_message(callback.from_user.id, callback.message.message_id)

            result = data["count_is_set"] == data["count_pack"]
            msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                       reply_markup=other_keyboards.get_product_btn(to_box=True, full=result))

            data["msg_link"] = msg["message_id"]

            await FSMSetBox.next()
        else:
            await callback.answer("Здесь пока ничего нет")
            return


@dp.callback_query_handler(text="back", state=FSMSetBox.choice_count_in_box)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        category = data["category"]

        text = f"{category['title']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        # msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
        #                            reply_markup=other_keyboards.get_category_btn())

        await callback.message.answer("Выберите сколько сладостей хотите пололжить в коробку",
                                      reply_markup=other_keyboards.choice_count_places_in_boxes())

        # data["msg_link"] = msg["message_id"]

        await FSMSetBox.previous()


## SHOW PREVIOUS PRODUCT

@dp.callback_query_handler(text="-", state=FSMSetBox.choice_category)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["product_index"] - 1 < data["product_start_index"]:
            await callback.answer("Это самое начало")
            return
        category_id = data["category"]["category_id"]
        data["product_index"] -= 1
        # product = get_product_table()[data["product_index"]]
        product = get_from_category_product(category_id)[data["product_index"]]
        data["product"] = product

        text = f"{product['title']}\nЦена: {product['price']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        result = data["count_is_set"] == data["count_pack"]
        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn(to_box=True, full=result))

        data["msg_link"] = msg["message_id"]


## SHOW PREVIOUS PRODUCT

@dp.callback_query_handler(text="+", state=FSMSetBox.choice_category)
async def next_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["product_index"] + 1 > data["product_end_index"]:
            await callback.answer("Это был последний")
            return
        category_id = data["category"]["category_id"]
        data["product_index"] += 1
        # product = get_product_table()[data["product_index"]]
        product = get_from_category_product(category_id)[data["product_index"]]
        data["product"] = product

        text = f"{product['title']}\nЦена: {product['price']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        result = data["count_is_set"] == data["count_pack"]
        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn(to_box=True, full=result))

        data["msg_link"] = msg["message_id"]


## SHOW STRUCTURE OF THE PRODUCT

@dp.callback_query_handler(text="info_1", state=FSMSetBox.choice_category)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = data["product"]

        product_info = f"Состав: {product['structure']}"

    await callback.answer(product_info, show_alert=True)


## SHOW INFO ABOUT PRODUCT

@dp.callback_query_handler(text="info_2", state=FSMSetBox.choice_category)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        product = data["product"]

        product_info = f"Описание: {product['product_description']}"

    await callback.answer(product_info, show_alert=True)


## RETURN TO CHOICE CATEGORY

@dp.callback_query_handler(text="back", state=FSMSetBox.choice_category)
async def get_info_about_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        category = data["category"]

        text = f"{category['title']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        await bot.delete_message(callback.from_user.id, callback.message.message_id)

        msg = await bot.send_photo(callback.from_user.id, category["image_link"], text,
                                   reply_markup=other_keyboards.get_category_btn(to_box=True))

        data["msg_link"] = msg["message_id"]

        await FSMSetBox.previous()


@dp.callback_query_handler(text="add", state=FSMSetBox.choice_category)
async def add_product_in_box(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["count_is_set"] + 1 > data["count_pack"]:
            await callback.answer("Коробка уже переполнена")
            return

        title_product = data["product"]["title"]
        category = data["category"]
        # if category["category_title"] in data["product_basket"]:

        if title_product in data["basket"]:
            data["basket"][title_product] += 1
            data["basket_price"][title_product] = data["product"]["price"]
            data["product_basket"][category["title"]][title_product]["count"] += 1
            # data["product_basket"][category["title"]][title_product]["price"] = data["product"]["price"]

        else:
            data["basket"][title_product] = 1
            data["basket_price"][title_product] = data["product"]["price"]
            data["product_basket"][category["title"]][title_product] = {"count": 1, "price": data["product"]["price"]}
        product = data["product"]

        data["all_price"] += product["price"]

        text = f"{product['title']}"

        data["count_is_set"] += 1
        await callback.answer("Добавлено")

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        result = data["count_is_set"] == data["count_pack"]
        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn(to_box=True, full=result))

        data["msg_link"] = msg["message_id"]


@dp.callback_query_handler(text="delete", state=FSMSetBox.choice_category)
async def delete_product_from_box(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["count_is_set"] == 0:
            await callback.answer("Коробка уже пустая")
            return

        category = data["category"]
        title_product = data["product"]["title"]
        if title_product in data["basket"]:

            data["basket"][title_product] -= 1
            data["product_basket"][category["title"]][title_product]["count"] -= 1
        else:
            await callback.answer("Вы такой еще не добавляли")
            return

        product = data["product"]

        data["all_price"] -= product["price"]

        text = f"{product['title']}"

        data["count_is_set"] -= 1
        await callback.answer("Добавлено")

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        # result = data["count_is_set"] == data["count_pack"]
        msg = await bot.send_photo(callback.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn(to_box=True))

        data["msg_link"] = msg["message_id"]


@dp.callback_query_handler(text="continue", state=FSMSetBox.choice_category)
async def delete_product_from_box(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    await callback.message.answer("Выберите тип доставки",
                                  reply_markup=other_keyboards.choice_type_delivery_btn())
    await FSMSetBox.next()


@dp.message_handler(Text(equals="Доставка", ignore_case=True), state=FSMSetBox.choice_product)
async def choice_type_as_delivery(msg: types.Message, state: FSMContext):
    await msg.answer("Введите адрес, куда нужно будет отвезти подарок или нажмите кнопку, "
                     "передать свое местоположение",
                     reply_markup=other_keyboards.set_location_user())

    await FSMSetBox.next()


@dp.message_handler(Text(equals="Самовывоз", ignore_case=True), state=FSMSetBox.choice_product)
async def choice_type_as_delivery(msg: types.Message, state: FSMContext):
    location = {
        "type": "self"
    }

    async with state.proxy() as data:
        data["location"] = location
        year_start = datetime.datetime.today().year
        data["year_start"] = year_start
        await msg.answer("Вы сможете забрать товар по этому адресу: ..",
                         reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
        await msg.answer("Теперь выберите дату",
                         reply_markup=other_keyboards.get_calendar_years(year_start))

    await FSMSetBox.choice_address.set()


@dp.message_handler(Text(equals="Назад", ignore_case=True), state=FSMSetBox.choice_product)
async def choice_type_as_delivery(msg: types.Message, state: FSMContext):
    await msg.answer("Выберите продукт",
                     reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

    async with state.proxy() as data:

        product = data["product"]

        text = f"{product['title']}\nЦена: {product['price']}"

        if data["count_is_set"] > 0:
            text += f"\n\nВаша корзина:"
            for elem in data["basket"]:
                text += f"\n{elem} - {data['basket'][elem]}шт."

        text += f"\n\nОбщая сумма: {data['all_price']}"

        await bot.delete_message(msg.from_user.id, msg.message_id)

        result = data["count_is_set"] == data["count_pack"]
        msg = await bot.send_photo(msg.from_user.id, product["image_link"], text,
                                   reply_markup=other_keyboards.get_product_btn(to_box=True, full=result))

        data["msg_link"] = msg["message_id"]

    await FSMSetBox.previous()


@dp.message_handler(content_types=['location'], state=FSMSetBox.choice_type_delivery)
async def set_location_with_button(msg: types.Message, state: FSMContext):
    location = {
        "type": "button",
        "latitude": msg.location.latitude,
        "longitude": msg.location.longitude
    }
    async with state.proxy() as data:
        data["location"] = location

        year_start = datetime.datetime.today().year
        data["year_start"] = year_start
        await msg.answer("Место доставки сохранено",
                         reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
        await msg.answer("Теперь выберите дату",
                         reply_markup=other_keyboards.get_calendar_years(year_start))

    await FSMSetBox.choice_address.set()


@dp.message_handler(state=FSMSetBox.choice_type_delivery)
async def set_location_with_input(msg: types.Message, state: FSMContext):
    location = {
        "type": "input",
        "address": msg.text
    }
    async with state.proxy() as data:
        data["location"] = location

        year_start = datetime.datetime.today().year
        data["year_start"] = year_start
        await msg.answer("Место доставки сохранено", reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
        await msg.answer("Теперь выберите дату",
                         reply_markup=other_keyboards.get_calendar_years(year_start))

    await FSMSetBox.choice_address.set()


@dp.message_handler(Text(equals="Назад", ignore_case=True), state=FSMSetBox.choice_type_delivery)
async def choice_type_as_delivery(msg: types.Message, state: FSMContext):
    await bot.delete_message(msg.from_user.id, msg.message_id)

    await msg.answer("Выберите тип доставки",
                     reply_markup=other_keyboards.choice_type_delivery_btn())

    await FSMSetBox.previous()


# START CHOICE DATE FOR DELIVERY

@dp.callback_query_handler(text="ignore", state=FSMSetBox.choice_address)
async def calendar_ignore_btn_year(callback: types.CallbackQuery):
    await callback.answer()


@dp.callback_query_handler(text="-", state=FSMSetBox.choice_address)
async def calendar_set_previous_year(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        actual_year = datetime.datetime.today().year
        if data["year_start"] - 5 < actual_year:
            await callback.answer("В прошлое не доставляем")
            data["year_start"] = actual_year
        else:
            data["year_start"] -= 5
        await callback.message.edit_reply_markup(other_keyboards.get_calendar_years(data["year_start"]))


@dp.callback_query_handler(text="+", state=FSMSetBox.choice_address)
async def calendar_set_next_year(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data["year_start"] += 5
        await callback.message.edit_reply_markup(other_keyboards.get_calendar_years(data["year_start"]))


@dp.callback_query_handler(Text(startswith="year"), state=FSMSetBox.choice_address)
async def calendar_set_year_to_month(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        async with state.proxy() as data:
            data["year_order"] = int(callback.data.split()[1])

            await callback.message.edit_text("Веберите месяц",
                                             reply_markup=other_keyboards.get_calendar_month(data["year_order"]))
            await FSMSetBox.next()
    except Exception:
        await callback.answer("Должно быть число")


@dp.callback_query_handler(text="back", state=FSMSetBox.choice_address)
async def calendar_set_year_to_month(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    await bot.delete_message(msg.from_user.id, msg.message_id)

    await msg.answer("Выберите тип доставки",
                     reply_markup=other_keyboards.choice_type_delivery_btn())

    await FSMSetBox.choice_product.set()


@dp.callback_query_handler(text="back_to_year", state=FSMSetBox.set_year)
async def calendar_set_year(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        order_year = data["year_order"]
        await callback.message.edit_text("Веберите год",
                                         reply_markup=other_keyboards.get_calendar_years(order_year))
        await FSMSetBox.choice_address.set()


@dp.callback_query_handler(text="ignore", state=FSMSetBox.set_year)
async def calendar_ignore_btn_month(callback: types.CallbackQuery):
    await callback.answer()


@dp.callback_query_handler(text="-", state=FSMSetBox.set_year)
async def calendar_set_year(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        actual_year = datetime.datetime.today().year
        if data["year_order"] - 1 < actual_year:
            await callback.answer("В прошлое не доставляем")
            await callback.answer()
            return
        data["year_order"] -= 1
        await callback.message.edit_reply_markup(other_keyboards.get_calendar_month(data["year_order"]))


@dp.callback_query_handler(text="+", state=FSMSetBox.set_year)
async def calendar_set_year(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data["year_order"] += 1
        await callback.message.edit_reply_markup(other_keyboards.get_calendar_month(data["year_order"]))


@dp.callback_query_handler(Text(startswith="month"), state=FSMSetBox.set_year)
async def calendar_set_year_to_month(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            month_order = int(callback.data.split()[1]) + 1
            today = datetime.datetime.today()
            actual_year = today.year
            actual_month = today.month
            if actual_year == data["year_order"] and actual_month > month_order:
                await callback.answer("В прошлое не доставляем")
                return
            data["month_order"] = month_order

            await callback.message.edit_text("Веберите день\nВыберите, пожалуйста, за 3 дня",
                                             reply_markup=other_keyboards.get_calendar_day(data["year_order"],
                                                                                           data["month_order"]))
            await FSMSetBox.next()
    except Exception:
        await callback.answer("Должно быть число")


@dp.callback_query_handler(text="back_to_year", state=FSMSetBox.set_mount)
async def calendar_set_year(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        order_year = data["year_order"]
        await callback.message.edit_text("Веберите год",
                                         reply_markup=other_keyboards.get_calendar_years(order_year))
        await FSMSetBox.choice_address.set()


@dp.callback_query_handler(text="back_to_month", state=FSMSetBox.set_mount)
async def calendar_set_year(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        order_year = data["year_order"]
        await callback.message.edit_text("Веберите месяц",
                                         reply_markup=other_keyboards.get_calendar_month(order_year))
        await FSMSetBox.set_year.set()


@dp.callback_query_handler(Text(startswith="day"), state=FSMSetBox.set_mount)
async def calendar_set_year_to_month(callback: types.CallbackQuery, state: FSMContext):
    # try:
        async with state.proxy() as data:
            day_order = int(callback.data.split()[1])
            today = datetime.datetime.today()
            actual_year = today.year
            actual_month = today.month
            actual_day = today.day
            if actual_year == data["year_order"] and actual_month == data["month_order"]:
                if actual_day > day_order:
                    await callback.answer("В прошлое не доставляем")
                    return

            d0 = datetime.date(actual_year, actual_month, actual_day)
            d1 = datetime.date(data['year_order'], data["month_order"], day_order)
            if (d1 - d0).days < 3:
                await callback.answer("Выберите, пожалуйста, за 3 дня")
                return
            data["day_order"] = day_order

            await callback.message.delete()

            await callback.message.answer("А теперь введите свой номер\nНужно нажать на кнопку",
                                          reply_markup=other_keyboards.set_contact_user())
            await FSMSetBox.next()
    # except Exception:
    #     await callback.answer("Должно быть число")


@dp.message_handler(content_types=["contact"], state=FSMSetBox.set_day)
async def set_contact(msg: types.Message, state: FSMContext):
    contact = msg["contact"]["phone_number"]
    async with state.proxy() as data:
        data["contact"] = str(contact)
        await msg.answer(get_text_for_client_check(data))
    await msg.answer("Можете написать комментарий к своему заказу",
                     reply_markup=other_keyboards.get_for_comment_btn())
    await FSMSetBox.next()


@dp.message_handler(Text(equals="Назад", ignore_case=True), state=FSMSetBox.set_day)
async def set_contact(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:

        await msg.answer("Веберите день",
                         reply_markup=other_keyboards.get_calendar_day(data["year_order"],
                                                                          data["month_order"]))
        await FSMSetBox.set_mount.set()


@dp.message_handler(state=FSMSetBox.get_user_contact)
async def set_contact(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text == "Завершить заказ":
            comment = "*Без комментариев*"
        else:
            comment = msg.text
        user_id = msg.from_user.id
        date = datetime.datetime.today().date()
        order_year = data["year_order"]
        order_month = data["month_order"]
        order_day = data["day_order"]
        order_date = f"{order_year}-{order_month}-{order_day}"
        location = data["location"]
        if location["type"] == "button":
            delivery_type = "Доставка"
            to_place = f"{data['location']['latitude']} - {data['location']['longitude']}"
        elif location["type"] == "input":
            delivery_type = "Доставка"
            to_place = data["location"]["address"]
        else:
            delivery_type = "самовывоз"
            to_place = "Нет"
        count_packet = 1
        user_phone = data["contact"]
        status = "ACTUAL"
        result = add_orders_in_table(user_id, date, order_date, delivery_type, to_place, count_packet, user_phone, comment, status)
        if result:
            order_id = get_orders_table()[-1]["order_id"]
            basket = data["basket"]
            basket_price = data["basket_price"]

            result = add_new_solds_packs(data["product_basket"], order_id)

            await msg.answer("Ваша заявка отправлена!",
                             reply_markup=other_keyboards.start_keyboards())
            # await bot.send_message("404248385", "Добавлен новый заказ")
            await bot.send_message("961023982", "Добавлен новый заказ")
            for elem in ADMINS:
                await bot.send_message(f"{elem}", "Добавлен новый заказ")
        else:
            await msg.answer("Произошла ошибка",
                             reply_markup=other_keyboards.start_keyboards())
            # await bot.send_message("404248385", "Произошла ошибка")
            await bot.send_message("961023982", "Произошла ошибка")
            for elem in ADMINS:
                await bot.send_message(f"{elem}", "Произошла ошибка")
        await state.finish()


# SHOW ASK-ANSWER

@dp.message_handler(Text(equals="Частые вопросы", ignore_case=True))
async def show_ask(msg: types.Message):
    ask_answer_list = get_list_ask()
    await msg.answer("Выберите вопрос",
                     reply_markup=other_keyboards.get_user_asks(ask_answer_list))

    await FSMUserAsks.status.set()


@dp.message_handler(state=FSMUserAsks.status)
async def show_answer(msg: types.Message):
    ask = msg.text
    answer = get_from_ask_answer(ask)
    await msg.answer(f"{ask}:\n\n{answer}")


@dp.message_handler(Text(equals="Задать вопрос", ignore_case=True))
async def user_choice_set_ticket(msg: types.Message):
    await msg.answer("Введите свой вопрос",
                     reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

    await FSMSetTicket.status.set()


@dp.message_handler(state=FSMSetTicket.status)
async def show_answer(msg: types.Message):
    user_id = msg.from_user.id
    new_ticket = msg.text
    result = add_user_ticket_in_table(user_id, new_ticket, "ACTUAL")
    if result:
        await msg.answer("Скоро администратор ответит на Ваш вопрос")
        # await bot.send_message("404248385", "Добавлен новый тикет от пользователя")
        await bot.send_message("961023982", "Добавлен новый тикет от пользователя")
        for elem in ADMINS:
            await bot.send_message(f"{elem}", "Добавлен новый тикет от пользователя")


# @dp.message_handler()
# async def input_add_admin_key(msg: types.Message):
#     if msg.text in ADD_ADMIN_KEYS:
#         print("okey")
#         await msg.answer("Нужно ввести Ваш номер, для этого нажмите на кнопку",
#                          reply_markup=other_keyboards.set_contact_user())
#         await FSMAddAdmin.input_key.set()








# @dp.message_handler(state=FSMShowProduct.choice_category_product)
# async def show_products(msg: types.Message, state: FSMContext):
#     data_product = get_products()
#
#     if data_product:
#         async with state.proxy() as data:
#             data["all_price"] = 0
#             data["basket"] = {}
#             data["category"] = msg.text
#
#             data["id_product"] = 0
#
#             products = [elem for elem in data_product if elem[6] == msg.text][data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#
#             await FSMShowProduct.next()
#
#             data["image_link"] = products[3]
#
#             msg_one = await msg.answer("Веберите продукт", reply_markup=other_keyboards.choice_product())
#             data["msg_one"] = msg_one["message_id"]
#
#             msg_two = await msg.answer_photo(products[3], text,
#                                  reply_markup=other_keyboards.get_product_btn())
#             data["msg_two"] = msg_two["message_id"]
#
#     else:
#         await msg.answer("Пока ничего нет")
#
#     # await bot.send_photo(msg.from_user.id, products[3], text,
#     #                      reply_markup=other_keyboards.get_product_btn())
#     # await msg.answer(text, reply_markup=other_keyboards.get_product_btn())


# PACKING PRESENTS

# QA

# SET ASK

#
#
# async def authorization_mail(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         user = get_user(msg.text)
#         if user[0]:
#             data["mail"] = msg.text
#             await FSMAuthorization.next()
#             await msg.answer("Введите свой пароль: ")
#         else:
#             await msg.answer("Аккаунта с такой почтой не найдено.")
#     await msg.delete()
#
#
# # @dp.message_handler(state=FSMAuthorization.password)
# async def authorization_password(msg: types.Message, state: FSMContext):
#
#     async with state.proxy() as data:
#         user = get_user(data["mail"])
#         if msg.text == user[1][3]:
#             user_id = str(msg.from_user.id)
#             await msg.answer("Добропожаловать! Вы вошли в свой аккаунт.",
#                              reply_markup=client_keyboards.start_keyboards())
#             ACCOUNTS[user_id] = "client"
#             if user[1][4] == "admin":
#                 await msg.answer("Аккаунт администратора запущен.", reply_markup=admin_keyboards.start_admin())
#                 # ADMINS.append(str(msg.from_user.id))
#                 ACCOUNTS[user_id] = "admin"
#                 ADMINS.append(user_id)
#             await state.finish()
#         else:
#             await msg.answer("Некорректно введен пароль.")
#
#     await msg.delete()
#
#
# # @dp.message_handler(state=FSMReg.login)
# async def reg_mail(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         user = get_user(msg.text)[0]
#         if user:
#             await msg.answer("Такая почта уже использовалась.")
#         else:
#             data["mail"] = msg.text
#             await msg.answer("Введите свой телефон, для этого нажмите на кнопку: ",
#                              reply_markup=client_keyboards.set_contact_user())
#             await FSMReg.next()
#
#     await msg.delete()
#
#
# async def reg_phone(msg: types.Message, state: FSMContext):
#     phone = msg["contact"]["phone_number"]
#     async with state.proxy() as data:
#         data["phone"] = phone
#     await msg.answer("Теперь введите пароль для своего аккаунта.")
#
#     await FSMReg.next()
#
#     await msg.delete()
#
#
# # @dp.message_handler(state=FSMReg.password)
# async def reg_password(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["password"] = msg.text
#         result = add_user(data["mail"], str(data["phone"]), data["password"])
#         print(data["mail"], str(data["phone"]), data["password"])
#         if result:
#             await msg.answer("Ваш аккаунт успешно создан!")
#         else:
#             await msg.answer("Произошла ошибка.")
#     await state.finish()
#
#     await msg.delete()
#
#
# async def show_all_test(msg: types.Message):
#     data = get_users()
#     await msg.answer(f"{data}")
#
#
# async def show_acc_test(msg: types.Message):
#     await msg.answer(f"{ACCOUNTS}")
#
#
# async def show_products_test(msg: types.Message):
#     result = get_products()
#     if result[0]:
#         data = result[1]
#         for elem in data:
#             text = f"{elem[1]}\nОписание: {elem[2]}\nСтоимость {elem[4]} руб."
#             await bot.send_photo(msg.from_user.id, elem[3], text)
#     # if data:
#     #
#     #     await msg.answer(data)
#
# #
# # @dp.message_handler(content_types=["contact"])
# # async def test(msg: types.Contact):
# #     print(msg["contact"]["phone_number"])
#
# ##################################################################
print("")
#
# async def show_product_category(msg: types.Message):
#     data = get_category()
#     if data:
#         await FSMShowProduct.choice_category_product.set()
#         list_btn = [elem[1] for elem in data]
#         await msg.answer("Выберите категорию товара.", reply_markup=other_keyboards.get_category_btn(list_btn))
#     else:
#         await msg.answer("Пока ничего нет")
#
#
# @dp.callback_query_handler(text="-", state=FSMShowProduct.choice_product)
# async def func_1(callback: types.CallbackQuery, state: FSMContext):
#
#     async with state.proxy() as data:
#         message = callback.message.text
#         category = data["category"]
#         if data["id_product"] == 0:
#             await callback.answer("Пока больше нет.")
#             return
#         data["id_product"] = data["id_product"] - 1
#
#         data_product = get_products()
#
#         products = [elem for elem in data_product if elem[6] == category][data["id_product"]]
#         text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#
#         data["image_link"] = products[3]
#
#         text_msg = ""
#         for elem in data["basket"]:
#             text_msg += f"{elem}: {data['basket'][elem]['count']} шт.\n"
#
#     msg = f"{text}\n{'#' * 10}\nВаша корзина: \n{text_msg}"
#
#     await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#     msg_two = await bot.send_photo(callback.from_user.id, products[3], msg,
#                          reply_markup=other_keyboards.get_product_btn())
#     data["msg_two"] = msg_two["message_id"]
#
#     # await callback.message.edit_text(msg, reply_markup=other_keyboards.get_product_btn())
#
#
# @dp.callback_query_handler(text="+", state=FSMShowProduct.choice_product)
# async def func_2(callback: types.CallbackQuery, state: FSMContext):
#
#     async with state.proxy() as data:
#         message = callback.message.text
#         category = data["category"]
#         data_product = get_products()
#
#         products = [elem for elem in data_product if elem[6] == category]
#
#         if data["id_product"] == len(products) - 1:
#             await callback.answer("Пока больше нет.")
#             return
#
#         data["id_product"] = data["id_product"] + 1
#         products = products[data["id_product"]]
#         text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#
#         data["image_link"] = products[3]
#
#         text_msg = ""
#         for elem in data["basket"]:
#             text_msg += f"{elem}: {data['basket'][elem]['count']} шт.\n"
#
#         msg = f"{text}\n{'#' * 10}\nВаша корзина: \n{text_msg}"
#
#         # await bot.edit_message_media(callback.from_user.id, products[3],
#         #                              reply_markup=other_keyboards.get_product_btn())
#
#         await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#         msg_two = await bot.send_photo(callback.from_user.id, products[3], msg,
#                              reply_markup=other_keyboards.get_product_btn())
#         data["msg_two"] = msg_two["message_id"]
#
#     # await callback.message.edit_text(msg, reply_markup=other_keyboards.get_product_btn())
#
#
# @dp.callback_query_handler(text="info", state=FSMShowProduct.choice_product)
# async def func_1(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         message = callback.message.text
#         category = data["category"]
#
#         data_product = get_products()
#
#         product_info = [elem for elem in data_product if elem[6] == category][data["id_product"]][5]
#
#     await callback.answer(product_info, show_alert=True)
#
#
# @dp.callback_query_handler(text="add_to_buy", state=FSMShowProduct.choice_product)
# async def func_1(callback: types.CallbackQuery, state: FSMContext):
#     text = f""
#     async with state.proxy() as data:
#
#         category = data["category"]
#         data_product = get_products()
#
#         products = [elem for elem in data_product if elem[6] == category]
#         products = products[data["id_product"]]
#
#         title = products[1]
#         if title in data["basket"]:
#             data["basket"][title]["count"] += 1
#         else:
#             data["basket"][title] = {"cost": int(products[4]), "count": 1}
#         for elem in data["basket"]:
#             text += f"{elem}: {data['basket'][elem]['count']} шт.\n"
#
#         msg_text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#         data["all_price"] += products[4]
#
#         # msg = f"{message.split('#'*10)[0].strip()}\n{'#'*10}\nВаша корзина: \n{text}"
#         msg = f"{msg_text}\n{'#' * 10}\nВаша корзина: \n{text}"
#
#         await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#         msg_two = await bot.send_photo(callback.from_user.id, data["image_link"], msg,
#                              reply_markup=other_keyboards.get_product_btn())
#         data["msg_two"] = msg_two["message_id"]
#
#     # await callback.message.edit_text(msg, reply_markup=other_keyboards.get_product_btn())
#
#
# @dp.callback_query_handler(text="del_from_basket", state=FSMShowProduct.choice_product)
# async def func_1(callback: types.CallbackQuery, state: FSMContext):
#     text = f""
#     async with state.proxy() as data:
#
#         data_product = get_products()
#         category = data["category"]
#         products = [elem for elem in data_product if elem[6] == category]
#         products = products[data["id_product"]]
#         title = products[1]
#
#         if title in data["basket"]:
#             data["basket"][title]["count"] -= 1
#             if data["basket"][title]["count"] == 0:
#                 del data["basket"][title]
#         else:
#             await callback.answer("Таких бомбочек нет в корзие.")
#             return
#
#         for elem in data["basket"]:
#             text += f"{elem}: {data['basket'][elem]['count']} шт.\n"
#
#         msg_text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#         data["all_price"] -= products[4]
#
#         # msg = f"{message.split('#' * 10)[0].strip()}\n{'#' * 10}\nВаша корзина: \n{text}"
#         msg = f"{msg_text}\n{'#' * 10}\nВаша корзина: \n{text}"
#
#         await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#         msg_two = await bot.send_photo(callback.from_user.id, data["image_link"], msg,
#                              reply_markup=other_keyboards.get_product_btn())
#         data["msg_two"] = msg_two["message_id"]
#
#     # await bot.delete_message(callback.from_user.id, callback.message.message_id)
#     #
#     # await bot.send_photo(callback.from_user.id, products[3], msg,
#     #                      reply_markup=other_keyboards.get_product_btn())
#
#     # await callback.message.edit_text(msg, reply_markup=other_keyboards.get_product_btn())
#
#
# @dp.message_handler(state=FSMShowProduct.choice_category_product)
# async def show_products(msg: types.Message, state: FSMContext):
#     data_product = get_products()
#
#     if data_product:
#         async with state.proxy() as data:
#             data["all_price"] = 0
#             data["basket"] = {}
#             data["category"] = msg.text
#
#             data["id_product"] = 0
#
#             products = [elem for elem in data_product if elem[6] == msg.text][data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#
#             await FSMShowProduct.next()
#
#             data["image_link"] = products[3]
#
#             msg_one = await msg.answer("Веберите продукт", reply_markup=other_keyboards.choice_product())
#             data["msg_one"] = msg_one["message_id"]
#
#             msg_two = await msg.answer_photo(products[3], text,
#                                  reply_markup=other_keyboards.get_product_btn())
#             data["msg_two"] = msg_two["message_id"]
#
#     else:
#         await msg.answer("Пока ничего нет")
#
#     # await bot.send_photo(msg.from_user.id, products[3], text,
#     #                      reply_markup=other_keyboards.get_product_btn())
#     # await msg.answer(text, reply_markup=other_keyboards.get_product_btn())
#
#
# async def choice_type_packet(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         pack = {"pack_one": [], "pack_two": [], "pack_three": [], "pack_four": []}
#         data["pack"] = pack
#
#         await FSMShowProduct.next()
#         await bot.delete_message(msg.from_user.id, data["msg_one"])
#         await bot.delete_message(msg.from_user.id, data["msg_two"])
#         await msg.answer("Вам перемешать товары разных типов?",
#                          reply_markup=other_keyboards.choice_yes_no())
#
#
# @dp.callback_query_handler(text="+", state=FSMShowProduct.choice_type_pack)
# async def func1(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data["random_type_pack"] = True
#         data["num_pack"] = 0
#         data["rows_packet"] = []
#
#         sum_product = 0
#
#         for elem in data["basket"]:
#             data["rows_packet"].extend([elem]*data["basket"][elem]["count"])
#             sum_product += data["basket"][elem]["count"]
#         data["num_product"] = sum_product
#         await FSMShowProduct.next()
#         text = f"А теперь давайте расфасуем продукцию.\n\nВсего {data['num_product']} продуктов"
#
#         await callback.message.answer(text,
#                                       reply_markup=other_keyboards.choice_packet_num())
#         print(data["rows_packet"])
#         await callback.answer()
#
#
# @dp.callback_query_handler(text="-", state=FSMShowProduct.choice_type_pack)
# async def func2(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data["random_type_pack"] = False
#         data["copy_basket"] = data["basket"]
#         data["rows_packet"] = []
#
#         await FSMShowProduct.next()
#
#         text = ""
#         for elem in data["basket"]:
#             data["rows_packet"].append([elem]*data["basket"][elem]["count"])
#             text += f"{elem}: {data['basket'][elem]['count']} шт.\n"
#
#         text_msg = f"А теперь давайте расфасуем продукцию.\n\nВсего {text}"
#         await callback.message.answer(text_msg,
#                                       reply_markup=other_keyboards.choice_packet_num())
#         await callback.answer()
#
#
# @dp.callback_query_handler(text="1", state=FSMShowProduct.choice_pack)
# async def func(callback: types.CallbackQuery, state: FSMContext):
#     num = 1
#     async with state.proxy() as data:
#         data["packing"] = []
#         if data["random_type_pack"]:
#             if len(data["rows_packet"]) >= num:
#                 data["pack"]["pack_one"].append(data["rows_packet"][:num])
#                 data["rows_packet"] = data["rows_packet"][num:]
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         else:
#
#             if len(data["rows_packet"][0]) >= num:
#                 data["pack"]["pack_one"].append(data["rows_packet"][0][:num])
#                 data["rows_packet"][0] = data["rows_packet"][0][num:]
#                 if len(data["rows_packet"][0]) == 0:
#                     data["rows_packet"].pop(0)
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         await callback.answer()
#         text = ""
#         ii = 1
#         for elem in data["pack"]:
#             print(elem)
#             for pack in data["pack"][elem]:
#                 print(pack)
#                 text += f"Упаковка {ii}: | {', '.join(pack)} |\n"
#                 ii += 1
#         await callback.message.answer(f"Получилось: {text}")
#
#         if not data["rows_packet"]:
#             await callback.message.answer("Все расфасовано. Теперь укажите адрес: ")
#             await FSMShowProduct.next()
#
#
# @dp.callback_query_handler(text="2", state=FSMShowProduct.choice_pack)
# async def func(callback: types.CallbackQuery, state: FSMContext):
#     num = 2
#     async with state.proxy() as data:
#         data["packing"] = []
#         if data["random_type_pack"]:
#             if len(data["rows_packet"]) >= num:
#                 data["pack"]["pack_two"].append(data["rows_packet"][:num])
#                 data["rows_packet"] = data["rows_packet"][num:]
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         else:
#
#             if len(data["rows_packet"][0]) >= num:
#                 data["pack"]["pack_two"].append(data["rows_packet"][0][:num])
#                 data["rows_packet"][0] = data["rows_packet"][0][num:]
#                 if len(data["rows_packet"][0]) == 0:
#                     data["rows_packet"].pop(0)
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         await callback.answer()
#
#         text = ""
#         ii = 1
#         for elem in data["pack"]:
#             print(elem)
#             for pack in data["pack"][elem]:
#                 print(pack)
#                 text += f"Упаковка {ii}: | {', '.join(pack)} |\n"
#                 ii += 1
#
#         await callback.message.answer(f"Получилось: {text}")
#
#         if not data["rows_packet"]:
#             await callback.message.answer("Все расфасовано. Теперь укажите адрес: ")
#             await FSMShowProduct.next()
#
#
# @dp.callback_query_handler(text="3", state=FSMShowProduct.choice_pack)
# async def func(callback: types.CallbackQuery, state: FSMContext):
#     num = 3
#     async with state.proxy() as data:
#         data["packing"] = []
#         if data["random_type_pack"]:
#             if len(data["rows_packet"]) >= num:
#                 data["pack"]["pack_three"].append(data["rows_packet"][:num])
#                 data["rows_packet"] = data["rows_packet"][num:]
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         else:
#
#             if len(data["rows_packet"][0]) >= num:
#                 data["pack"]["pack_three"].append(data["rows_packet"][0][:num])
#                 data["rows_packet"][0] = data["rows_packet"][0][num:]
#                 if len(data["rows_packet"][0]) == 0:
#                     data["rows_packet"].pop(0)
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         await callback.answer()
#
#         text = ""
#         ii = 1
#         for elem in data["pack"]:
#             print(elem)
#             for pack in data["pack"][elem]:
#                 print(pack)
#                 text += f"Упаковка {ii}: | {', '.join(pack)} |\n"
#                 ii += 1
#
#         await callback.message.answer(f"Получилось: {text}")
#
#         if not data["rows_packet"]:
#             await callback.message.answer("Все расфасовано. Теперь укажите адрес: ")
#             await FSMShowProduct.next()
#
#
# @dp.callback_query_handler(text="4", state=FSMShowProduct.choice_pack)
# async def func(callback: types.CallbackQuery, state: FSMContext):
#     num = 4
#     async with state.proxy() as data:
#         data["packing"] = []
#         if data["random_type_pack"]:
#             if len(data["rows_packet"]) >= num:
#                 data["pack"]["pack_four"].append(data["rows_packet"][:num])
#                 data["rows_packet"] = data["rows_packet"][num:]
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         else:
#
#             if len(data["rows_packet"][0]) >= num:
#                 data["pack"]["pack_four"].append(data["rows_packet"][0][:num])
#                 data["rows_packet"][0] = data["rows_packet"][0][num:]
#                 if len(data["rows_packet"][0]) == 0:
#                     data["rows_packet"].pop(0)
#             else:
#                 await callback.answer("Продуктов меньше, чем мест в коробке", show_alert=True)
#                 return
#         await callback.answer()
#
#         text = ""
#         ii = 1
#         for elem in data["pack"]:
#             print(elem)
#             for pack in data["pack"][elem]:
#                 print(pack)
#                 text += f"Упаковка {ii}: | {', '.join(pack)} |\n"
#                 ii += 1
#
#         await callback.message.answer(f"Получилось: {text}")
#
#         if not data["rows_packet"]:
#             await callback.message.answer("Все расфасовано. Теперь укажите адрес: ")
#             await FSMShowProduct.next()
#
#
# @dp.message_handler(state=FSMShowProduct.choice_address)
# async def func(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["address"] = msg.text
#         data["distance"] = find_distance(msg.text)
#         price = find_sum(data["basket"], data["pack"], data["distance"])
#         data["approx_sum"] = round(price, 2)
#
#         await msg.answer(f"Примерная стоимость вашего заказа: {round(price, 2)}р.")
#         await msg.answer("Теперь введите дату, на которую хотите получить товар.")
#
#         await FSMShowProduct.next()
#
#
# @dp.message_handler(state=FSMShowProduct.choice_date)
# async def func(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["date"] = msg.text
#
#         await msg.answer("Введите свой контакт, для этого нажмите на кнопку",
#                          reply_markup=other_keyboards.set_contact_user())
#
#         await FSMShowProduct.next()
#
#
# # @dp.message_handler(state=FSMShowProduct.check_user_status)
# # async def func(msg: types.Message, state: FSMContext):
# #     pass
#
#
# @dp.message_handler(content_types=["contact"], state=FSMShowProduct.get_user_contact)
# async def func(msg: types.Message, state: FSMContext):
#     user_id = msg.from_user.id
#     contact = msg["contact"]["phone_number"]
#     async with state.proxy() as data:
#         data["contact"] = str(contact)
#
#         add_orders(user_id, data["basket"], data["date"], data["address"],
#                    str(data["distance"]), data["contact"], str(datetime.now().date()), data["approx_sum"], data["pack"])
#
#     await msg.answer("Заказ сохранен", reply_markup=other_keyboards.start_keyboards())
#     await bot.send_message("404248385", "Добавлен новый заказ")
#
#     await state.finish()
#
#
# @dp.message_handler(Text(equals="Собрать подарки", ignore_case=True))
# async def start_build_packet(msg: types.Message):
#     await FSMSetBox.choice_count_of_box.set()
#     await msg.answer("Введите количество коробок:",
#                      reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
#
#
# @dp.message_handler(state=FSMSetBox.choice_count_of_box)
# async def set_count_of_box(msg: types.Message, state: FSMContext):
#     try:
#         count = int(msg.text)
#         async with state.proxy() as data:
#             data["box_count"] = count
#             data["box_dict"] = dict()
#             for elem in range(count):
#                 data["box_dict"][elem] = 0
#             data["boxes"] = [list() for ii in range(count)]
#             data["box_index"] = 0
#
#         await FSMSetBox.next()
#
#         text = "Теперь давайте выберем размер для каждой коробки\n\n"
#         text += f"Итого упаковок: {data['box_count']}\n\n"
#         for elem in data["box_dict"]:
#             text += f"Упаковка {elem + 1}: {data['box_dict'][elem]} бомбочек\n"
#
#         await msg.answer(text,
#                          reply_markup=other_keyboards.choice_count_places_in_boxes())
#
#
#
#     except Exception:
#         await msg.answer("Вы ввели не число, попробуйте еще раз")
#
#
# @dp.callback_query_handler(Text(startswith="count_pack"), state=FSMSetBox.choice_type_of_box)
# async def choice_count(callback: types.CallbackQuery, state: FSMContext):
#     # try:
#     async with state.proxy() as data:
#         data["box_dict"][data["box_index"]] = int(callback.data.split()[1])
#         data["box_index"] += 1
#         #
#         text = "Теперь давайте выберем размер для каждой коробки\n\n"
#         text += f"Итого упаковок: {data['box_count']}\n\n"
#         for elem in data["box_dict"]:
#             text += f"Упаковка {elem + 1}: {data['box_dict'][elem]} бомбочек\n"
#         await callback.message.edit_text(text,
#                                          reply_markup=other_keyboards.choice_count_places_in_boxes())
#
#         if data["box_index"] == data["box_count"]:
#             await FSMSetBox.next()
#             await callback.message.answer("Теперь давайте заполним упаковки!")
#             data = get_category()
#             if data:
#                 list_btn = [elem[1] for elem in data]
#                 await callback.message.answer("Выберите категорию товара.", reply_markup=other_keyboards.get_category_btn(list_btn))
#
#                 await FSMSetBox.next()
#             else:
#                 await callback.message.answer("Пока ничего нет")
#
#         await callback.answer()
#
#     # except Exception:
#     #     pass
#
#
# @dp.message_handler(state=FSMSetBox.choice_category)
# async def choice_category(msg: types.Message, state: FSMContext):
#     data_product = get_products()
#
#     if data_product:
#         async with state.proxy() as data:
#             data["all_price"] = 0
#             data["basket"] = {}
#             data["category"] = msg.text
#
#             data["id_product"] = 0
#
#             products = [elem for elem in data_product if elem[6] == msg.text][data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#
#             await FSMShowProduct.next()
#
#             data["image_link"] = products[3]
#
#             msg_one = await msg.answer("Веберите продукт", reply_markup=other_keyboards.choice_product())
#             data["msg_one"] = msg_one["message_id"]
#
#             msg_two = await msg.answer_photo(products[3], text,
#                                              reply_markup=other_keyboards.get_product_btn())
#             data["msg_two"] = msg_two["message_id"]
#
#     else:
#         await msg.answer("Пока ничего нет")
#
#
# # @dp.message_handler(state=FSMSetBox.choice_product)
# # async def choice_product(msg: types.Message, state: FSMContext):
# #     pass
#
#
#
#
#
# # @dp.message_handler(state=FSMSetBox.choice_type_of_box)
# # async def choice_type_of_box(msg: types.Message, state: FSMContext):
# #     try:
# #         num_place_in_box = int(msg.text)
# #         async with state.proxy() as data:
# #             data["boxes"][data["box_index"]] = num_place_in_box
# #             data["box_index"] += 1
# #             print(data["box_count"])
# #
# #             text = ""
# #             for elem in range(len(data["boxes"])):
# #                 text += f"Коробка {elem}: на {data['boxes'][elem]} мест\n"
# #             if data["box_index"] == data["box_count"]:
# #                 await FSMSetBox.next()
# #                 await msg.answer("Теперь давайте перейдем к выбору продукции.")
# #                 return
# #             await msg.edit_text(f"Сейчас у вас \n{text}")
# #             # await msg.answer(f"Продолжим. Сейчас у вас \n{text}")
# #     except Exception as ex:
# #         await msg.answer("Выберите из предложенных вариантов.")
# #         print(ex)
#
#
# # @dp.message_handler(state=FSMSetBox.choice_category)
#
#
#
#
#
#
# async def log_in(msg: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if not current_state is None:
#         await state.finish()
#
#     await FSMAuthorization.mail.set()
#     await msg.reply("Введите свой mail.", reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
#
#
# async def sign_in(msg: types.Message):
#     await FSMReg.mail.set()
#     await msg.reply("Для регистрации введите свой mail", reply_markup=other_keyboards.create_keyboards(list(),
#                                                                                      cancel_btn=True))
#
#
# async def user_asks(msg: types.Message, state: FSMContext):
#
#     data_asks = get_user_asks()
#     if data_asks:
#         await FSMUserAsks.status.set()
#         async with state.proxy() as data:
#             data["asks_dict"] = dict()
#             for elem in data_asks:
#                 data["asks_dict"][elem[1]] = elem[2]
#             asks_list = list(data["asks_dict"].keys())
#             await msg.answer("Выберите вопрос, который Вас интересует.",
#                              reply_markup=other_keyboards.get_user_asks(asks_list))
#
#     else:
#         await msg.answer("Пока ничего нет")
#
#
# async def get_answer(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         await msg.answer(data["asks_dict"][msg.text])
#
#
# async def text_filter(msg: types.Message, state=None):
#     # user_id = msg.from_user.id
#     message_text = msg.text
#
#     if message_text == "Посмотреть товар":
#         await msg.answer("Пока ничего нет..")
#
#     elif message_text == "Войти":
#         await FSMAuthorization.mail.set()
#         await msg.reply("Введите свой mail", reply_markup=ReplyKeyboardRemove())
#
#     elif message_text == "Зарегистрироваться":
#         await FSMReg.mail.set()
#         await msg.reply("Для регистрации введите свой mail", reply_markup=ReplyKeyboardRemove())
#
#
# def register_handlers_other(disp: Dispatcher):
#     disp.register_message_handler(start, commands=["start"], state="*")
#     disp.register_message_handler(cancel, Text(equals="Отмена", ignore_case=True), state="*")
#     disp.register_message_handler(show_product_category, Text(equals="Посмотреть товар", ignore_case=True))
#     disp.register_message_handler(log_in, Text(equals="Войти", ignore_case=True))
#     disp.register_message_handler(log_in, commands=["log_in"], state="*")
#     disp.register_message_handler(sign_in, Text(equals="Зарегистрироваться", ignore_case=True))
#     disp.register_message_handler(user_asks, Text(equals="Частые вопросы", ignore_case=True))
#     disp.register_message_handler(choice_type_packet, Text(equals="Перейти к выбору упаковки", ignore_case=True),
#                                   state=FSMShowProduct.choice_product)
#
#     # disp.register_message_handler(show_all_test, commands=["show_users"])
#     # disp.register_message_handler(show_acc_test, commands=["show_acc"])
#     disp.register_message_handler(get_answer, state=FSMUserAsks.status)
#     # disp.register_message_handler(show_products, state=FSMShowProduct.choice_category_product)
#     disp.register_message_handler(authorization_mail, state=FSMAuthorization.mail)
#     disp.register_message_handler(authorization_password, state=FSMAuthorization.password)
#     disp.register_message_handler(reg_mail, state=FSMReg.mail)
#     disp.register_message_handler(reg_phone, content_types=["contact"], state=FSMReg.phone)
#     disp.register_message_handler(reg_password, state=FSMReg.password)
#     disp.register_message_handler(text_filter)
#
#
# #
# # @dp.message_handler(state=FSMReg.login)
# # async def input_login(msg: types.Message, state: FSMReg):
# #     pass
#
# #
# # @dp.message_handler(content_types=["photo"], state=FSMReg.photo)
# # async def load_photo(msg: types.Message, state: FSMReg):
# #     async with state.proxy() as data:
# #         data["photo"] = msg.photo[0].file_id
# #     await FSMReg.next()
#
# # @dp.message_handler(state=None)
# # async def reg_start(msg: types.Message):
# #     await FSMReg.login.set()
# #     await msg.reply("Input login: ")
