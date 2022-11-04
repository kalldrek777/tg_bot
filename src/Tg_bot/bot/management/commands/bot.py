from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from django.conf import settings
from isdayoff import DateType, ProdCalendar
import aioschedule
from datetime import datetime, timedelta, date
import os
from ..commands.sqlite import db_start, create_profile, get_users, delete_profile
import time
import schedule
import asyncio
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from ast import literal_eval
from aiohttp import BasicAuth
# from aiohttp

auth = BasicAuth(login='kalldrek', password='kalldrek777')

TOKEN = settings.TOKEN

calendar = ProdCalendar(locale='ru')

bot = Bot(token=TOKEN, proxy='socks5://98.142.251.6:1080', proxy_auth=auth)
dp = Dispatcher(bot)

button = KeyboardButton('/stop')
button_2 = KeyboardButton('/start')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)
greet_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_2)


async def day():
    list = []
    mist = []
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    res = await calendar.range_date(
        (datetime.today() + timedelta(days=1)),
        (datetime.today() + timedelta(days=8)))
    for k, v in res.items():
        if v == DateType.NOT_WORKING:
            list.append(k)
    for i in list:
        a = i.split('.')
        b = i + "-" + weekdays[datetime(int(a[0]), int(a[1]), int(a[2])).weekday()]
        mist.append(b)
    return mist


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await bot.send_message(message.from_user.id, 'Вы остановили бота', reply_markup=greet_kb_2)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # global id
    id = message.from_user.id
    await create_profile(user_id=id)
    mist = await day()
    await bot.send_message(id, 'На следующей неделе у вас выходные:' '\n' + '\n'.join(
                '{}'.format(item) for item in mist), reply_markup=greet_kb)



async def gg():
    mist = await day()
    users = await get_users()
    for user in users:
        try:
            await bot.send_message(user[0], 'На следующей неделе у вас выходные:' '\n' + '\n'.join('{}'.format(item) for item in mist), reply_markup=greet_kb)
        except:
            pass


async def scheduler():
    aioschedule.every().sunday.do(gg)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    await db_start()
    asyncio.create_task(scheduler())


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# from django.core.management.base import BaseCommand
# from django.conf import settings
# import telegram
# import schedule
# from isdayoff import DateType, ProdCalendar
# from datetime import datetime, timedelta, date
# import time
# import asyncio
# from telegram import Bot, Update
# from telegram.utils.request import Request
# from telegram.ext import Updater, MessageHandler,Filters,CallbackContext
# from bot.models import User
#
# calendar = ProdCalendar(locale='ru')
#
#
# def log_errors(f):
#
#     def inner(*args, **kwargs):
#         try:
#             return f(*args, **kwargs)
#         except Exception as e:
#             error_message = f'Произошла ошибка: {e}'
#             print(error_message)
#             raise e
#     return inner
#
# async def main():
#         res = await calendar.range_date(
#             (datetime.today() + timedelta(days=1)),
#             (datetime.today() + timedelta(days=8)))
#         # count = len([DateType.NOT_WORKING for day in res if res[day] == DateType.NOT_WORKING])
#         for k, v in res.items():
#             if v == DateType.NOT_WORKING:
#                 list.append(k)
#         return list
# @log_errors
# def do_echo(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     text = update.message.text
#
#     p,_ = User.objects.get_or_create(
#         external_id=chat_id,
#     )
#
#     list = []
#
#     loop = asyncio.get_event_loop()
#     loop.create_task(main())
#
#     loop.run_forever()
#
#     # bob = main()
#
#     reply_text_2 = "На следующей неделе у вас выходные дни: {}".format(bob)
#     update.message.reply_text(
#         text=reply_text_2,
#     )
#
#
#
#
# class Command(BaseCommand):
#     help = 'Телеграм-бот'
#     list = []
#
#     def handle(self, *args, **options):
#         request = Request(
#             connect_timeout=0.5,
#             read_timeout=1.0,
#         )
#         bot = Bot(
#             request=request,
#             token=settings.TOKEN,
#         )
#
#         # async def main():
#         #     # c = 1
#         #     # while True:
#         #     #     c+=1
#         #     #     await asyncio.sleep(1)
#         #     res = await calendar.range_date(
#         #     (datetime.today() + timedelta(days=1)),
#         #     (datetime.today() + timedelta(days=8)))
#         #     count = len([DateType.NOT_WORKING for day in res if res[day] == DateType.NOT_WORKING])
#         #     list = []
#         #     for k, v in res.items():
#         #         if v == DateType.NOT_WORKING:
#         #             list.append(k)
#         #     print(list)
#         #
#         # loop = asyncio.get_event_loop()
#         # loop.create_task(main())
#         # loop.run_forever()
#
#
#         print(bot.get_me())
#
#
#         updater = Updater(
#             bot=bot,
#             use_context=True,
#         )
#
#         message_handler = MessageHandler(Filters.text, do_echo) # schedule.every().sunday.at('13:12').do(   -   время публикации
#         updater.dispatcher.add_handler(message_handler)
#
#         updater.start_polling()
#         updater.idle()
