from aiogram import types, Dispatcher
from start_bot import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_keyboards, admin_keyboards, other_keyboards
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from add_function import get_histogram

from data_base import add_users_in_table
from data_base import add_sold_pack_in_table
from data_base import add_product_in_table
from data_base import add_orders_in_table
from data_base import add_ask_answer_in_table
from data_base import add_admin_in_table
from data_base import add_user_ticket_in_table
from data_base import add_category_in_table
from data_base import get_users_table
from data_base import get_ask_answer_table
from data_base import get_category_table
from data_base import get_orders_table
from data_base import get_product_table
from data_base import get_user_ticket_table
from data_base import get_sold_pack_table
from data_base import get_list_category
from data_base import get_id_from_title_category
from data_base import del_category_from_table
from data_base import get_from_category_product
from data_base import del_product_from_table
from data_base import get_from_category_product_title
from data_base import update_phone_user
from data_base import update_password_user
from data_base import get_list_ask
from data_base import del_ask_answer_from_table
from data_base import get_user_ticket_table
from data_base import get_from_order_sold
from data_base import get_orders_table
from data_base import update_status_order
from data_base import update_status_user_ticket
from data_base import get_actual_order
from data_base import get_actual_user_ticket

from handlers.other import ADMINS, ADD_ADMIN_KEYS


# from add_function import get_info_order
# from add_function import get_histogram



class FSMAddProductCategory(StatesGroup):
    title = State()
    describe = State()


class FSMAddUserAsk(StatesGroup):
    ask = State()
    answer = State()


class FSMAddProduct(StatesGroup):
    category = State()
    title = State()
    description = State()
    image = State()
    price = State()
    structure = State()


class FSMDelProduct(StatesGroup):
    choice_category = State()
    del_product = State()


class FSMSettings(StatesGroup):
    choice_settings = State()
    choice_category = State()
    choice_add_category = State()
    input_title = State()
    input_description = State()
    input_image_link_for_category = State()
    choice_update_category = State()
    choice_category_for_update = State()
    choice_param_for_update = State()
    update_category_title = State()
    update_category_description = State()
    choice_delete_category = State()
    choice_category_for_delete = State()
    accept_category_for_delete = State()

    choice_product = State()
    choice_add_product = State()
    choice_category_for_add_product = State()
    input_title_product = State()
    input_description_for_product = State()
    input_structure_for_product = State()
    input_price_for_product = State()
    input_image_link_for_product = State()
    choice_update_product = State()
    choice_param_for_update_product = State()
    update_title_product = State()
    update_description_for_product = State()
    update_structure_for_product = State()
    update_price_for_product = State()
    update_image_link_for_product = State()
    choice_category_for_product_delete = State()
    choice_delete_product = State()
    choice_product_for_delete = State()

    choice_ask_answer = State()
    choice_add_ask_answer = State()
    input_ask = State()
    input_answer = State()
    choice_update_ask_answer = State()
    choice_param_for_update_ask_answer = State()
    update_adk = State()
    update_answer = State()
    choice_delete_ask_answer = State()
    choice_ask_answer_for_delete = State()

    choice_account = State()
    choice_param_for_update_account = State()
    choice_update_phone = State()
    choice_update_password = State()
    accept_update_password = State()

    choice_add_admin = State()
    create_admin_key = State()
    input_new_admin_key = State()
    input_reverse_admin_key = State()
    delete_admin_key = State()


class FSMShow(StatesGroup):

    choice_type_of_ticket = State()
    show_user_ticket = State()
    answer_on_user_ticket = State()

    choice_type_of_order = State()
    show_user_order = State()
    answer_on_user_order = State()

    show_analytic = State()
    choice_type_one = State()
    choice_type_two = State()
    choice_type_three = State()


def get_text_for_show_order_to_admin(order):
    if order["type_deliver"] in ["Доставка"]:
        address = f"Адрес: {order['to_place']}\n"
    else:
        address = ""

    if order["status"] in ["ACTUAL"]:
        status = "Актуально"
    else:
        status = "Просмотрено"

    if order["user_comment"]:
        comment = f"Комментарий пользователя: {order['user_comment']}\n"
    else:
        comment = ""

    basket_text = "\nКорзина:\n"
    basket = get_from_order_sold(order["order_id"])
    print(basket)
    all_price = 0
    for elem in basket:
        basket_text += f"{elem['product_title']}\nКатегория: {elem['category_title']}\n" \
                       f"Количество: {elem['count']}\nЦена: {elem['one_price']}\n"
        all_price += elem['count'] * elem['one_price']

    text = f"Дата заказа: {order['order_date']}\nСтатус: {status}\n" \
           f"К дате: {order['to_date']}\nТип доставки: {order['type_deliver']}\n{address}" \
           f"Номер пользователя: {order['user_phone']}\n{comment}\n{basket_text}\nВсего: {all_price}"

    return text


@dp.message_handler(commands=["log_out"])
async def log_out(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        ADMINS.remove(user_id)
        await bot.send_message(msg.from_user.id, "Добропожаловать!",
                               reply_markup=other_keyboards.start_keyboards())


@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        current_state = await state.get_state()
        print(current_state)
        # if current_state is None:
        #     return

        if current_state:
            await state.finish()
        await bot.send_message(msg.from_user.id, "Добропожаловать, Админ!",
                               reply_markup=admin_keyboards.start_admin())


@dp.message_handler(commands=["state"], state="*")
async def func(msg: types.Message, state: FSMContext):
    # user_id = str(msg.from_user.id)
    # if user_id in ADMINS:
    current_state = await state.get_state()
    if current_state is None:
        await msg.answer(f"Ваше состояние: None")
        return
    await msg.answer(f"Ваше состояние: {current_state}")


# START SETTINGS

@dp.message_handler(Text(equals="Настройки", ignore_case=True))
async def settings(msg: types.Message):
    print("ok")
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, что хотите настроить",
                         reply_markup=admin_keyboards.settings_btn())

        await FSMSettings.choice_settings.set()


## START SETTINGS CATEGORY

@dp.message_handler(Text(equals="Категории", ignore_case=True), state=FSMSettings.choice_settings)
async def settings_category(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую настройку хотите произвести",
                         reply_markup=admin_keyboards.settings_category_btn())

        await FSMSettings.choice_category.set()


### ADD NEW CATEGORY

@dp.message_handler(Text(equals="Создать", ignore_case=True), state=FSMSettings.choice_category)
async def settings_add_new_category(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Введите название для новой категории",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_add_category.set()


#### SET TITLE FOR CATEGORY

@dp.message_handler(state=FSMSettings.choice_add_category)
async def settings_add_new_category_set_title(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_title = msg.text
        if len(new_title) > 10:
            async with state.proxy() as data:
                data["category_title"] = new_title

            await msg.answer("Введите описание для новой категории\n(Должно быть меньше 150 символов)",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.input_title.set()
        else:
            await msg.answer("Введите более длинное название.")


#### SET DESCRIPTION FOR CATEGORY

@dp.message_handler(state=FSMSettings.input_title)
async def settings_add_new_category_set_description(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_description = msg.text
        if len(new_description) < 150:
            async with state.proxy() as data:
                data["category_description"] = new_description

            await msg.answer("Отправьте картинку для новой категории",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.input_description.set()
        else:
            await msg.answer("Описание превышает 150 символов. "
                             "Телеграм не сможет вывести такую информацию.")


#### SET IMAGE FOR CATEGORY

@dp.message_handler(content_types=["photo"], state=FSMSettings.input_description)
async def settings_add_new_category_set_image(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        image_link = msg.photo[0].file_id
        async with state.proxy() as data:
            data["category_image"] = image_link

        await msg.answer("Сохранить новую категорию?",
                         reply_markup=admin_keyboards.acception_btn())

        await FSMSettings.input_image_link_for_category.set()


#### SAVE INFORMATION FOR CATEGORY
@dp.message_handler(Text(equals="Да", ignore_case=True), state=FSMSettings.input_image_link_for_category)
async def settings_add_new_category_save(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:

        async with state.proxy() as data:
            title = data["category_title"]
            description = data["category_description"]
            image_link = data["category_image"]

            result = add_category_in_table(title, description, image_link)
        if result:
            await msg.answer("Новая категория успешно добавлена.",
                             reply_markup=admin_keyboards.start_admin())
        else:
            await msg.answer("Новая категория не добавлена.",
                             reply_markup=admin_keyboards.start_admin())

        await state.finish()


### UPDATE CATEGORY

@dp.message_handler(Text(equals="Изменить", ignore_case=True), state=FSMSettings.choice_category)
async def settings_update_category(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую категорию хотите изменить",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_update_category.set()


### DELETE CATEGORY

@dp.message_handler(Text(equals="Удалить", ignore_case=True), state=FSMSettings.choice_category)
async def settings_choice_delete_category(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        category_list = get_list_category()
        await msg.answer("Выберите какую категорию хотите удалить",
                         reply_markup=admin_keyboards.get_some_list_btn(category_list))

        await FSMSettings.choice_delete_category.set()


@dp.message_handler(state=FSMSettings.choice_delete_category)
async def settings_delete_category(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:

        category_title = msg.text
        product_is_exist = get_from_category_product(category_title)
        if product_is_exist:
            async with state.proxy() as data:
                data["category_title"] = category_title
                await msg.answer("Вы уверены, что хотите удалить категорию?\n"
                                 "Вместе с ней удалятся связанные с ней продукты",
                                 reply_markup=admin_keyboards.acception_btn())
                await FSMSettings.choice_category_for_delete.set()
        else:
            result = del_category_from_table(category_title)
            if result:
                await msg.answer("Категория удалена",
                             reply_markup=admin_keyboards.start_admin())

            await state.finish()


@dp.message_handler(Text(equals="Да", ignore_case=True), state=FSMSettings.choice_category_for_delete)
async def settings_choice_delete_category(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:

            result = del_category_from_table(data["category_title"])
            if result:
                await msg.answer("Категория удалена",
                                 reply_markup=admin_keyboards.start_admin())

            await state.finish()


## START SETTINGS PRODUCT

@dp.message_handler(Text(equals="Продукты", ignore_case=True), state=FSMSettings.choice_settings)
async def settings_product(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую настройку хотите произвести",
                         reply_markup=admin_keyboards.settings_product_btn())

        await FSMSettings.choice_product.set()


### ADD NEW PRODUCT

@dp.message_handler(Text(equals="Создать", ignore_case=True), state=FSMSettings.choice_product)
async def settings_add_new_product(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите категорию для нового продукта",
                         reply_markup=admin_keyboards.settings_product_category_btn(get_list_category()))

        await FSMSettings.choice_add_product.set()


#### SET CATEGORY FOR PRODUCT

@dp.message_handler(state=FSMSettings.choice_add_product)
async def settings_add_new_product_set_category(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        category = msg.text
        if category in get_list_category():
            async with state.proxy() as data:
                data["product_category"] = category
            await msg.answer("Введите название для нового продукта",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.choice_category_for_add_product.set()
        else:
            await msg.answer("Выберите вариант из предложенных")


#### SET TITLE FOR PRODUCT

@dp.message_handler(state=FSMSettings.choice_category_for_add_product)
async def settings_add_new_product_set_title(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_title = msg.text
        if len(new_title) > 5:
            async with state.proxy() as data:
                data["product_title"] = new_title
            await msg.answer("Введите описание для нового продукта\n(Должно быть меньше 150 символов)",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.input_title_product.set()
        else:
            await msg.answer("Введите более длинное название")


#### SET DESCRIPTION FOR PRODUCT

@dp.message_handler(state=FSMSettings.input_title_product)
async def settings_add_new_product_set_description(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_description = msg.text
        if len(new_description) < 150:
            async with state.proxy() as data:
                data["product_description"] = new_description
            await msg.answer("Введите состав для нового продукта\n(Должно быть меньше 150 символов)",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.input_description_for_product.set()
        else:
            await msg.answer("Описание превышает 150 символов. "
                             "Телеграм не сможет вывести такую информацию.")


#### SET STRUCTURE FOR PRODUCT

@dp.message_handler(state=FSMSettings.input_description_for_product)
async def settings_add_new_product_set_structure(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_structure = msg.text
        if len(new_structure) < 150:
            async with state.proxy() as data:
                data["product_structure"] = new_structure
            await msg.answer("Введите стоимость для нового продукта",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

            await FSMSettings.input_structure_for_product.set()
        else:
            await msg.answer("Состав превышает 150 символов."
                             "Телеграм не сможет вывести такую информацию.")


#### SET PRICE FOR PRODUCT

@dp.message_handler(state=FSMSettings.input_structure_for_product)
async def settings_add_new_product_set_price(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        try:
            new_price = int(msg.text)
            if new_price > 0:
                async with state.proxy() as data:
                    data["product_price"] = new_price
                await msg.answer("Отправьте картинку для нового продукта",
                                 reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

                await FSMSettings.input_price_for_product.set()
            else:
                await msg.answer("Введите положительную стоимость")
        except Exception:
            await msg.answer("введите число")


#### SET IMAGE FOR PRODUCT

@dp.message_handler(content_types=["photo"], state=FSMSettings.input_price_for_product)
async def settings_add_new_product_set_image(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_image = msg.photo[0].file_id
        async with state.proxy() as data:
            data["product_image"] = new_image
        await msg.answer("Сохранить данные?",
                         reply_markup=admin_keyboards.acception_btn())

        await FSMSettings.input_image_link_for_product.set()


#### SAVE NEW PRODUCT

@dp.message_handler(Text(equals="Да", ignore_case=True), state=FSMSettings.input_image_link_for_product)
async def settings_add_new_product_save(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            category = data["product_category"]
            category_id = get_id_from_title_category(category)
            title = data["product_title"]
            description = data["product_description"]
            structure = data["product_structure"]
            price = data["product_price"]
            image_link = data["product_image"]

            result = add_product_in_table(category_id, title, description, structure, price, image_link)
        if result:
            await msg.answer("Новый продукт успешно добавлен.",
                             reply_markup=admin_keyboards.start_admin())
        else:
            await msg.answer("Новый продукт не добавлен.",
                             reply_markup=admin_keyboards.start_admin())

        await state.finish()


### UPDATE PRODUCT

@dp.message_handler(Text(equals="Изменить", ignore_case=True), state=FSMSettings.choice_product)
async def settings_update_product(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую категорию хотите изменить",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_update_product.set()


### DELETE PRODUCT

@dp.message_handler(Text(equals="Удалить", ignore_case=True), state=FSMSettings.choice_product)
async def settings_delete_product(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        category_list = get_list_category()
        await msg.answer("Выберите категорию в которой хотите удалить продукт",
                         reply_markup=admin_keyboards.get_some_list_btn(category_list))

        await FSMSettings.choice_category_for_product_delete.set()


@dp.message_handler(state=FSMSettings.choice_category_for_product_delete)
async def settings_delete_product(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            category_title = msg.text
            data["category_title"] = category_title
            category_id = get_id_from_title_category(category_title)
            product_list = get_from_category_product_title(category_id)

            await msg.answer("Выберите какой продукт хотите удалить",
                             reply_markup=admin_keyboards.get_some_list_btn(product_list))

            await FSMSettings.choice_delete_product.set()


@dp.message_handler(state=FSMSettings.choice_delete_product)
async def settings_delete_product(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            product = msg.text
            category_id = get_id_from_title_category(data["category_title"])
            result = del_product_from_table(product, category_id)
            if result:
                await msg.answer("Продукт успешно удален",
                                 reply_markup=admin_keyboards.start_admin())

                await state.finish()


## START SETTINGS ASK-ANSWER

@dp.message_handler(Text(equals="Вопрос-ответ", ignore_case=True), state=FSMSettings.choice_settings)
async def settings_ask_answer(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую настройку хотите произвести",
                         reply_markup=admin_keyboards.settings_ask_answer_btn())

        await FSMSettings.choice_ask_answer.set()


### ADD NEW ASK-ANSWER

@dp.message_handler(Text(equals="Создать", ignore_case=True), state=FSMSettings.choice_ask_answer)
async def settings_add_ask_answer(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Введите новый вопрос",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_add_ask_answer.set()


@dp.message_handler(state=FSMSettings.choice_add_ask_answer)
async def settings_add_ask_answer_set_ask(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_ask = msg.text
        async with state.proxy() as data:
            data["ask_answer_ask"] = new_ask

        await msg.answer("Введите ответ на этот вопрос",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.input_ask.set()


@dp.message_handler(state=FSMSettings.input_ask)
async def settings_add_ask_answer_set_answer(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_answer = msg.text
        async with state.proxy() as data:
            data["ask_answer_answer"] = new_answer

        await msg.answer("Сохранить данный?",
                         reply_markup=admin_keyboards.acception_btn())

        await FSMSettings.input_answer.set()


@dp.message_handler(Text(equals="Да", ignore_case=True), state=FSMSettings.input_answer)
async def settings_add_ask_answer_save(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            ask = data["ask_answer_ask"]
            answer = data["ask_answer_answer"]

            result = add_ask_answer_in_table(ask, answer)
        if result:
            await msg.answer("Новые вопрос-ответ успешно добавлены.",
                             reply_markup=admin_keyboards.start_admin())
        else:
            await msg.answer("Новые вопрос-ответ не добавлены.",
                             reply_markup=admin_keyboards.start_admin())

        await state.finish()


### UPDATE ASK-ANSWER

@dp.message_handler(Text(equals="Изменить", ignore_case=True), state=FSMSettings.choice_ask_answer)
async def settings_update_ask_answer(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую категорию хотите изменить",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_update_ask_answer.set()


### DELETE ASK-ANSWER

@dp.message_handler(Text(equals="Удалить", ignore_case=True), state=FSMSettings.choice_ask_answer)
async def settings_delete_ask_answer(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        ask_list = get_list_ask()
        if ask_list:
            await msg.answer("Выберите какой вопрос удалить",
                             reply_markup=admin_keyboards.get_some_list_btn(ask_list))
        else:
            await msg.answer("Здесь ничего нет",
                             reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_delete_ask_answer.set()


@dp.message_handler(state=FSMSettings.choice_delete_ask_answer)
async def settings_delete_ask_answer(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        ask_list = get_list_ask()
        ask = msg.text
        if ask in ask_list:
            result = del_ask_answer_from_table(ask)
            if result:
                await msg.answer("Вопрос успешно удален",
                                 reply_markup=admin_keyboards.start_admin())
            else:
                await msg.answer("Произошла ошибка",
                                 reply_markup=admin_keyboards.start_admin())
            await state.finish()
        else:
            await msg.answer("Выберите вопрос из предложенных")


## START SETTINGS ACCOUNT

@dp.message_handler(Text(equals="Аккаунт", ignore_case=True), state=FSMSettings.choice_settings)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите, какую настройку хотите произвести",
                         reply_markup=admin_keyboards.settings_account_btn())

        await FSMSettings.choice_param_for_update_account.set()


@dp.message_handler(Text(equals="Изменить номер", ignore_case=True), state=FSMSettings.choice_param_for_update_account)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Для изменения телефона, нажмите на кнопку",
                         reply_markup=other_keyboards.set_contact_user())

        await FSMSettings.choice_update_phone.set()


@dp.message_handler(content_types=["contact"], state=FSMSettings.choice_update_phone)
async def set_contact(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        contact = msg["contact"]["phone_number"]
        result = update_phone_user(user_id, contact)
        if result:

            await msg.answer("Ваш телефон изменен",
                             reply_markup=admin_keyboards.start_admin())
        else:
            await msg.answer("Произошла ошибка",
                             reply_markup=admin_keyboards.start_admin())
        await state.finish()


@dp.message_handler(Text(equals="Изменить пароль", ignore_case=True), state=FSMSettings.choice_param_for_update_account)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Введите новый пароль",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.choice_update_password.set()


@dp.message_handler(state=FSMSettings.choice_update_password)
async def settings_account(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        new_password = msg.text
        await msg.delete()
        async with state.proxy() as data:
            data["new_password"] = new_password
        await msg.answer("Подтвердите свой новый пароль")

        await FSMSettings.accept_update_password.set()


@dp.message_handler(state=FSMSettings.accept_update_password)
async def settings_account(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        access_password = msg.text
        await msg.delete()
        async with state.proxy() as data:
            if data["new_password"] == access_password:
                result = update_password_user(user_id, access_password)
                if result:
                    await msg.answer("Пароль успешно изменен")
                else:
                    await msg.answer("Произошла ошибка")
            else:
                await msg.answer("Пароли не совпадают")

        await state.finish()


# SHOW USERS TICKETS

@dp.message_handler(Text(equals="Посмотреть тикеты клиентов", ignore_case=True))
async def settings_account(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Загрузка тикетов пользователей",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))
        await msg.answer("Хотите посмотреть все тикеты или только актуальные?",
                         reply_markup=admin_keyboards.get_type_ticket_order_status_btn())

        await FSMShow.choice_type_of_ticket.set()


@dp.callback_query_handler(Text(startswith="status"), state=FSMShow.choice_type_of_ticket)
async def settings_account(callback: types.CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            show_type = callback.data.split()[1]
            data["show_type"] = show_type

            if data["show_type"] == "actual":
                user_ticket_list = get_actual_user_ticket()
            else:
                user_ticket_list = get_user_ticket_table()
            msg = callback.message
            if user_ticket_list:

                data["ticket_index"] = 0
                data["ticket_start_index"] = 0
                data["ticket_end_index"] = len(user_ticket_list) - 1

                ticket = user_ticket_list[data["ticket_index"]]
                data["ticket"] = ticket

                text = f"{ticket['ask']}\nСтатус: {ticket['status']}"

                await msg.answer("Веберите вопрос",
                                 reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

                msg = await msg.answer(text,
                                       reply_markup=admin_keyboards.get_ticket_btn())

                data["msg_link"] = msg["message_id"]

                await FSMShow.show_user_ticket.set()
            else:
                await msg.answer("Пока ничего нет")


@dp.callback_query_handler(text="-", state=FSMShow.show_user_ticket)
async def previuos_ticket(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if data["show_type"] == "actual":
            user_ticket_list = get_actual_user_ticket()
        else:
            user_ticket_list = get_user_ticket_table()
        if data["ticket_index"] - 1 < data["ticket_start_index"]:
            await callback.answer("Это самое начало")
            return
        data["ticket_index"] -= 1
        ticket = user_ticket_list[data["ticket_index"]]
        data["ticket"] = ticket

        text = f"{ticket['ask']}\nСтатус: {ticket['status']}"
        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
            await callback.answer()
        else:
            await callback.answer()


@dp.callback_query_handler(text="+", state=FSMShow.show_user_ticket)
async def next_ticket(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if data["show_type"] == "actual":
            user_ticket_list = get_actual_user_ticket()
        else:
            user_ticket_list = get_user_ticket_table()
        ticket_end_index = len(user_ticket_list)
        if data["ticket_index"] + 1 > ticket_end_index:
            await callback.answer("Это самый конец")
            return
        data["ticket_index"] += 1
        ticket = user_ticket_list[data["ticket_index"]]
        data["ticket"] = ticket

        text = f"{ticket['ask']}\nСтатус: {ticket['status']}"
        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
        await callback.answer()


@dp.callback_query_handler(text="answer", state=FSMShow.show_user_ticket)
async def previuos_ticket(callback: types.CallbackQuery):
    await callback.message.answer("Введите сообщение для пользователя")

    await FSMShow.next()


@dp.message_handler(state=FSMShow.answer_on_user_ticket)
async def previuos_ticket(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ticket = data["ticket"]
        user_ticket_id = ticket["user_ticket_id"]
        user_id = ticket["user_id"]
        ask = ticket["ask"]
        text = f"Добрый день!\nАдминистратор ответил на Ваш вопрос ({ask}): {msg.text}"
        try:
            await bot.send_message(ticket['user_id'], text)
            result = update_status_user_ticket(user_ticket_id, "READ")
            if result:
                await msg.answer("Сообщение успешно отправлено")
            else:
                await msg.answer("Произошла ошибка")
        except Exception:
            await msg.answer("Произошла ошибка при отправке")

        await FSMShow.show_user_ticket.set()


@dp.callback_query_handler(text="change_status", state=FSMShow.show_user_ticket)
async def previuos_ticket(callback: types.CallbackQuery, state: FSMContext):
    async  with state.proxy() as data:
        ticket = data["ticket"]
        user_ticket_id = ticket["user_ticket_id"]
        result = update_status_user_ticket(user_ticket_id, "READ")
        if result:
            await callback.answer("Статус изменен")
            data["ticket"]["status"] = "READ"
        else:
            await callback.answer("Произошла ошибка", show_alert=True)

        text = f"{ticket['ask']}\nСтатус: {ticket['status']}"
        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
        await callback.answer()


# SHOW USERS ORDERS

@dp.message_handler(Text(equals="Посмотреть заказы", ignore_case=True))
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Загрузка заказов пользователей",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))
        await msg.answer("Хотите посмотреть все заказы или только актуальные?",
                         reply_markup=admin_keyboards.get_type_ticket_order_status_btn())

        await FSMShow.choice_type_of_order.set()


@dp.callback_query_handler(Text(startswith="status"), state=FSMShow.choice_type_of_order)
async def settings_account(callback: types.CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    if user_id in ADMINS:
        async with state.proxy() as data:
            show_type = callback.data.split()[1]
            data["show_type"] = show_type

            if data["show_type"] == "actual":
                order_list = get_actual_order()
            else:
                order_list = get_orders_table()
            msg = callback.message

        # order_list = get_orders_table()
        if order_list:
            async with state.proxy() as data:
                data["order_index"] = 0
                data["order_start_index"] = 0
                data["order_end_index"] = len(order_list) - 1

                order = order_list[data["order_index"]]
                data["order"] = order

                text = get_text_for_show_order_to_admin(order)

                await msg.answer("Веберите заказ",
                                 reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))

                msg = await msg.answer(text,
                                       reply_markup=admin_keyboards.get_order_btn())

                data["msg_link"] = msg["message_id"]

                await FSMShow.show_user_order.set()
        else:
            await msg.answer("Пока ничего нет")


@dp.callback_query_handler(text="-", state=FSMShow.show_user_order)
async def previuos_ticket(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if data["show_type"] == "actual":
            order_list = get_actual_order()
        else:
            order_list = get_orders_table()
        if data["order_index"] - 1 < data["order_start_index"]:
            await callback.answer("Это самое начало")
            return
        data["order_index"] -= 1
        order = order_list[data["order_index"]]
        data["order"] = order

        text = get_text_for_show_order_to_admin(order)

        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
            await callback.answer()
        else:
            await callback.answer()


@dp.callback_query_handler(text="+", state=FSMShow.show_user_order)
async def next_ticket(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if data["show_type"] == "actual":
            order_list = get_actual_order()
        else:
            order_list = get_orders_table()
        order_end_index = len(order_list) - 1
        if data["order_index"] + 1 > order_end_index:
            await callback.answer("Это самый конец")
            return
        data["order_index"] += 1
        order = order_list[data["order_index"]]
        data["order"] = order

        text = get_text_for_show_order_to_admin(order)

        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
        await callback.answer()


@dp.callback_query_handler(text="answer", state=FSMShow.show_user_order)
async def previuos_ticket(callback: types.CallbackQuery):
    await callback.message.answer("Введите сообщение для пользователя")

    await FSMShow.next()


@dp.message_handler(state=FSMShow.answer_on_user_order)
async def previuos_ticket(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        order = data["order"]
        order_id = order["order_id"]
        user_id = order["user_id"]
        comment = order["user_comment"]
        text = f"Добрый день!\nАдминистратор ответил на Ваш комментарий к заказу ({comment}): {msg.text}"
        try:
            await bot.send_message(order['user_id'], text)
            result = update_status_order(order_id, "READ")
            if result:
                await msg.answer("Сообщение успешно отправлено")
            else:
                await msg.answer("Произошла ошибка")
        except Exception:
            await msg.answer("Произошла ошибка при отправке")

        await FSMShow.show_user_order.set()


@dp.callback_query_handler(text="change_status", state=FSMShow.show_user_order)
async def previuos_ticket(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        order = data["order"]
        order_id = order["order_id"]
        if order['status'] == "ACTUAL":
            result = [update_status_order(order_id, "READ"), 1]
        else:
            result = [update_status_order(order_id, "ACTUAL"), 2]

        if result[0]:
            await callback.answer("Статус изменен")
            if result[1] == 1:
                data["order"]["status"] = "READ"
            else:
                data["order"]["status"] = "ACTUAL"
        else:
            await callback.answer("Произошла ошибка", show_alert=True)

        text = get_text_for_show_order_to_admin(order)
        if text != callback.message.text:
            await callback.message.edit_text(text,
                                             reply_markup=admin_keyboards.get_ticket_btn())
        await callback.answer()


# SHOW USERS ANALYTIC

@dp.message_handler(Text(equals="Посмотреть аналитику", ignore_case=True))
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Введите тип показа статистики",
                         reply_markup=admin_keyboards.get_analityc_btn())

        await FSMShow.show_analytic.set()


@dp.message_handler(Text(equals="Количество заказанных", ignore_case=True), state=FSMShow.show_analytic)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        diagram_name = "diagram.png"
        get_histogram(diagram_name, type_histogram=1)
        with open(diagram_name, 'rb') as img:
            print(0)
            await bot.send_photo(msg.from_user.id, img)

        # await FSMShow.choice_type_one.set()


@dp.message_handler(Text(equals="Общая стоимость заказанных", ignore_case=True), state=FSMShow.show_analytic)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        diagram_name = "diagram.png"
        get_histogram(diagram_name, type_histogram=2)
        with open(diagram_name, 'rb') as img:
            print(1)
            await bot.send_photo(msg.from_user.id, img)

        # await FSMShow.choice_type_two.set()


@dp.message_handler(Text(equals="Добавить нового администратора", ignore_case=True), state=FSMSettings.choice_settings)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer("Выберите режим",
                         reply_markup=admin_keyboards.settings_add_admin_btn())

        await FSMSettings.choice_add_admin.set()


@dp.message_handler(Text(equals="Создать ключ", ignore_case=True), state=FSMSettings.choice_add_admin)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        await msg.answer(f"Введите новый ключ, по которому можно будет создать один аккаунт Админа",
                         reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))

        await FSMSettings.create_admin_key.set()


@dp.message_handler(state=FSMSettings.create_admin_key)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        ADD_ADMIN_KEYS.append(msg.text)
        await msg.answer(f"Ключ сохранен, теперь второму пользователю нужно ввести /add_admin"
                         f", а затем '{msg.text}' в чат с ботом",
                         reply_markup=admin_keyboards.start_admin())

        await FSMSettings.input_new_admin_key.set()


@dp.message_handler(Text(equals="Удалить все ключи", ignore_case=True), state=FSMSettings.choice_add_admin)
async def settings_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id in ADMINS:
        ADD_ADMIN_KEYS.clear()
        await msg.answer("Ключи удалены",
                         reply_markup=admin_keyboards.start_admin())

        await FSMSettings.delete_admin_key.set()


# @dp.message_handler()
# async def input_add_admin_key(msg: types.Message):
#     if msg.text in ADD_ADMIN_KEYS:
#         print("okey")
#         await msg.answer("Нужно ввести Ваш номер, для этого нажмите на кнопку",
#                          reply_markup=other_keyboards.set_contact_user())
#         await FSMAddAdmin.input_key.set()



# add new product
#
# async def add_product_step0(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         category_list = list()
#         category = get_category()
#         if category:
#             for elem in category:
#                 category_list.append(elem[1])
#             await FSMAddProduct.category.set()
#             await msg.answer("Выберите в какую категорию хотите добавить новыйй продукт",
#                              reply_markup=admin_keyboards.get_category_product_btn(category_list))
#         else:
#             await msg.answer("Создайте категорию")
#
#
# async def add_product_step1(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["category"] = msg.text
#         await FSMAddProduct.next()
#         await msg.answer("Введите название для нового продукта.", reply_markup=ReplyKeyboardRemove())
#
#
# async def add_product_step2(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["title"] = msg.text
#         await FSMAddProduct.next()
#         await msg.answer("Введите описание для нового продукта.")
#
#
# async def add_product_step3(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["description"] = msg.text
#         await FSMAddProduct.next()
#         await msg.answer("Отправьте картинку для нового продукта.")
#
#
# async def add_product_step4(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["image"] = msg.photo[0].file_id
#             print(data["image"])
#         await FSMAddProduct.next()
#         await msg.answer("Введите цену для нового продукта.")
#
#
# async def add_product_step5(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["price"] = int(msg.text)
#         await FSMAddProduct.next()
#         await msg.answer("Введите состав.")
#
#
# async def add_product_step6(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#
#         async with state.proxy() as data:
#             result = add_product(data["title"], data["description"], data["image"],
#                                  data["price"], msg.text, data["category"])
#
#             if result:
#                 await msg.answer(f"{data['title']} добавлен.",
#                                  reply_markup=admin_keyboards.start_admin())
#
#             else:
#                 await msg.answer("Произошла ошибка.")
#
#         await state.finish()
#
#
# # add product category
#
# async def add_product_category(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#
#         await msg.answer("Введите название для новой категории.",
#                          reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))
#
#         await FSMAddProductCategory.title.set()
#
#
# async def add_category_step1(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["title"] = msg.text
#             await FSMAddProductCategory.next()
#             await msg.answer("Введите описание для категории.")
#
#
# async def add_category_step2(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             result = add_category_product(data["title"], msg.text)
#             if result:
#                 await msg.answer("Новая категория добавлена,")
#             else:
#                 await msg.answer("Произошла ошибка.")
#
#         await state.finish()
#
#
# # add ask-answer
#
# async def add_user_ask_step0(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#
#         await msg.answer("Введите вопрос.",
#                          reply_markup=admin_keyboards.create_keyboards(list(), cancel_btn=True))
#
#         await FSMAddUserAsk.ask.set()
#
#
# async def add_user_ask_step1(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["ask"] = msg.text
#             await FSMAddUserAsk.next()
#             await msg.answer("Введите ответ для этого вопроса.")
#
#
# async def add_user_ask_step2(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             result = add_user_ask(data["ask"], msg.text)
#             if result:
#                 await msg.answer("Вопрос и ответ добавлены,")
#             else:
#                 await msg.answer("Произошла ошибка.")
#
#         await state.finish()
#
#
# # Delete product
#
# async def delete_product(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         data = get_category()
#         if data:
#             list_btn = [elem[1] for elem in data]
#             await msg.answer("Выберите из какой категории продукт нужно удалить",
#                              reply_markup=other_keyboards.get_category_btn(list_btn))
#             await FSMDelProduct.choice_category.set()
#         else:
#             await msg.answer("Нет продуктов")
#
#
# async def delete_product_step1(msg: types.Message, state: FSMContext):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         async with state.proxy() as data:
#             data["category"] = msg.text
#             data["id_product"] = 0
#             data_product = get_products()
#
#             products = [elem for elem in data_product if elem[6] == msg.text][data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}"
#             data["title"] = products[1]
#
#             msg_one = await msg.answer("Веберите продукт для удаления",
#                                        reply_markup=other_keyboards.create_keyboards(list(), cancel_btn=True))
#             data["msg_one"] = msg_one["message_id"]
#
#             msg_two = await msg.answer_photo(products[3], text,
#                                  reply_markup=admin_keyboards.get_del_product_btn(products[1]))
#             data["msg_two"] = msg_two["message_id"]
#
#             await FSMDelProduct.next()
#
#
# @dp.callback_query_handler(text="-", state=FSMDelProduct.del_product)
# async def func_1(callback: types.CallbackQuery, state: FSMContext):
#     user_id = str(callback.from_user.id)
#     if user_id in ADMINS:
#
#         async with state.proxy() as data:
#             category = data["category"]
#             if data["id_product"] == 0:
#                 await callback.answer("Пока больше нет.")
#                 return
#             data["id_product"] = data["id_product"] - 1
#
#             data_product = get_products()
#
#             products = [elem for elem in data_product if elem[6] == category][data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}\nСостав: {products[5]}"
#
#             data["image_link"] = products[3]
#             data["title"] = products[1]
#
#         await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#     msg_two = await bot.send_photo(callback.from_user.id, products[3], text,
#                          reply_markup=admin_keyboards.get_del_product_btn(products[1]))
#
#     data["msg_two"] = msg_two["message_id"]
#
#
# @dp.callback_query_handler(text="+", state=FSMDelProduct.del_product)
# async def func_2(callback: types.CallbackQuery, state: FSMContext):
#     user_id = str(callback.from_user.id)
#     if user_id in ADMINS:
#
#         async with state.proxy() as data:
#             category = data["category"]
#             data_product = get_products()
#
#             products = [elem for elem in data_product if elem[6] == category]
#
#             if data["id_product"] == len(products) - 1:
#                 await callback.answer("Пока больше нет.")
#                 return
#
#             data["id_product"] = data["id_product"] + 1
#             products = products[data["id_product"]]
#             text = f"{products[1]}\n{products[2]}\nPrice: {products[4]}\nСостав: {products[5]}"
#
#             data["image_link"] = products[3]
#             data["title"] = products[1]
#
#             await bot.delete_message(callback.from_user.id, callback.message.message_id)
#
#             msg_two = await bot.send_photo(callback.from_user.id, products[3], text,
#                                  reply_markup=admin_keyboards.get_del_product_btn(products[1]))
#             data["msg_two"] = msg_two["message_id"]
#
#
# # @dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "), state=FSMDelProduct.del_product)
# async def del_product_step2(callback: types.CallbackQuery, state: FSMContext):
#     user_id = str(callback.from_user.id)
#     if user_id in ADMINS:
#         product_title = str(callback.data.replace("del ", ""))
#         result = del_product(product_title)
#
#         await callback.message.answer(result)
#         await callback.answer()
#
#
# # Show orders
# async def show_orders_admin(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         order_data = get_info_order()
#         if order_data[0]:
#             await msg.answer(order_data[2])
#         else:
#             await msg.answer("База заказов пуста")
#
#
# async def show_histogram_order(msg: types.Message):
#     user_id = str(msg.from_user.id)
#     if user_id in ADMINS:
#         diagram_name = "diagram.jpg"
#         get_histogram(diagram_name)
#         with open(diagram_name, 'rb') as img:
#             await bot.send_photo(msg.from_user.id, img)
#
#
# # Show sold
# async def show_sold(msg: types.Message):
#     pass
#
#
# async def change_product_list(msg: types.Message):
#     pass


states = [
    FSMAddProduct.title,
    FSMAddProduct.category,
    FSMAddProduct.description,
    FSMAddProduct.image,
    FSMAddProduct.price,
    FSMAddProduct.structure,
    FSMAddProductCategory.title,
    FSMAddProductCategory.describe,
    FSMAddUserAsk.ask,
    FSMAddUserAsk.answer,
    FSMDelProduct.choice_category,
    FSMDelProduct.del_product
]


def register_handlers_admin(disp: Dispatcher):
    disp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state="*")
    # disp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=FSMAddProduct.title)
    # disp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=FSMAddProduct.image)
    # disp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=FSMAddProduct.description)
    # disp.register_message_handler(add_product_step0, Text(equals="Добавить товар", ignore_case=True))
    # disp.register_message_handler(add_product_step1, state=FSMAddProduct.category)
    # disp.register_message_handler(add_product_step2, state=FSMAddProduct.title)
    # disp.register_message_handler(add_product_step3, state=FSMAddProduct.description)
    # disp.register_message_handler(add_product_step4, content_types=["photo"], state=FSMAddProduct.image)
    # disp.register_message_handler(add_product_step5, state=FSMAddProduct.price)
    # disp.register_message_handler(add_product_step6, state=FSMAddProduct.structure)
    # disp.register_message_handler(add_product_category, Text(equals="Добавить категорию", ignore_case=True))
    # disp.register_message_handler(add_category_step1, state=FSMAddProductCategory.title)
    # disp.register_message_handler(add_category_step2, state=FSMAddProductCategory.describe)
    # disp.register_message_handler(add_user_ask_step0, Text(equals="Добавить вопрос-ответ", ignore_case=True))
    # disp.register_message_handler(add_user_ask_step1, state=FSMAddUserAsk.ask)
    # disp.register_message_handler(add_user_ask_step2, state=FSMAddUserAsk.answer)
    #
    # disp.register_message_handler(show_orders_admin, Text(equals="Посмотреть заказы", ignore_case=True))
    # disp.register_message_handler(show_histogram_order, Text(equals="Посмотреть статистику", ignore_case=True))
    #
    # disp.register_message_handler(delete_product, Text(equals="Удалить товар", ignore_case=True))
    # disp.register_message_handler(delete_product_step1, state=FSMDelProduct.choice_category)
