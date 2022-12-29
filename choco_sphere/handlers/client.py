from aiogram import types, Dispatcher
from start_bot import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_keyboards, admin_keyboards, other_keyboards
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

# from aiogram.methods.edit_message_text import EditMessageText



from data_base import add_user, get_users, get_user, add_admin, get_products



async def edit_msg(message: types.Message):
    await message.edit_text("Так")



def register_handlers_client(disp: Dispatcher):
    pass
    # disp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=FSMAuthorization.password)