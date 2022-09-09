from django.core.management.base import BaseCommand
from django.conf import settings
import telegram
import schedule
from isdayoff import DateType, ProdCalendar
from datetime import datetime, timedelta
import time
from telegram import Bot, Update
from telegram.utils.request import Request
from telegram.ext import Updater, MessageHandler,Filters,CallbackContext
from bot.models import User

calendar = ProdCalendar(locale='ru')

def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    return inner

@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p,_ = User.objects.get_or_create(
        external_id=chat_id,
    )

    # days = calendar.range_date((datetime.now().year, datetime.now().month, datetime.today()+timedelta(days=1)), (datetime.now().year, datetime.now().month, datetime.today()+timedelta(days=8)))
    reply_text = "Ваш id = {}\n\n{}".format(chat_id, text)
    # reply_text_2 = "На следующей неделе у вас выходные дни: {}".format(days)
    update.message.reply_text(
        text=reply_text,
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, schedule.every().sunday.at('13:12').do(do_echo))
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()