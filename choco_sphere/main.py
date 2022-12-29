from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
import os
from start_bot import dp
from aiogram import types

# from handlers import client, admin, other
from handlers import admin, other
#
# from data_base import connecting


# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!\nНапиши мне что-нибудь!")
#
#
# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")
#
#
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     if msg.content_type == "text":
#         await bot.send_message(msg.from_user.id, msg.text)
#     else:
#         await bot.send_message(msg.from_user.id, "False")


async def on_startup(_):
    # connecting()
    print("Bot is starting!")

#
# admin.register_handlers_admin(dp)
# client.register_handlers_client(dp)
# other.register_handlers_other(dp)

@dp.message_handler(commands=["myid"])
async def func(msg: types.Message):
    await msg.reply(msg.from_user.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
