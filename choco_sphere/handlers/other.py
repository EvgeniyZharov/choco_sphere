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
from data_base import contact


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


@dp.message_handler(commands=["test_fuck_db"])
async def test(msg: types.Message):
    await msg.answer(f"users: {get_users_table()}")
    await msg.answer(f"category: {get_category_table()}")
    await msg.answer(f"product: {get_product_table()}")
    await msg.answer(f"orders: {get_orders_table()}")
    
    
@dp.message_handler(commands=["test_fuck_db_2"])
async def test(msg: types.Message):
    result = contact()
    await msg.answer(f"result: {str(result)}")


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
