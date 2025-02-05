# bot/telegram_bot.py
import os
import django
import asyncio
import threading
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram.utils import executor

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flshop.settings')

# Инициализируем Django
django.setup()

# Импортируем модель Order после настройки Django
from shop.models import Order

# Ваш токен бота
API_TOKEN = '8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())

# Функция уведомления о новом заказе
async def send_order_notification(order):
    # Здесь ваш код для отправки уведомлений
    pass

# Функция для обработки новых заказов
def notify_new_order(order):
    loop = asyncio.new_event_loop()  # Создаем новый цикл событий для потока
    asyncio.set_event_loop(loop)  # Устанавливаем новый цикл событий
    loop.run_until_complete(send_order_notification(order))  # Запускаем асинхронную задачу

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в магазин!")

# Другие обработчики для бота

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



# import os
# import logging
# from django.conf import settings
# from telegram import Bot
#
# # Указываем настройки Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flshop.settings')
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# TELEGRAM_BOT_TOKEN = os.environ.get('8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI', settings.TELEGRAM_BOT_TOKEN)
# TELEGRAM_SUPERADMIN_CHAT_ID = os.environ.get('1375390614', settings.TELEGRAM_SUPERADMIN_CHAT_ID)
#
# bot = Bot(token=TELEGRAM_BOT_TOKEN)
#
# async def send_order_notification(order):
#     message = (
#         f"*Новый заказ* №{order.pk}\n"
#         f"Пользователь: {order.user.username}\n"
#         f"Сумма заказа: {order.total_price}\n"
#         f"Дата доставки: {order.delivery_date}\n"
#         f"Время доставки: {order.delivery_time}\n"
#         f"Адрес доставки: {order.delivery_address}\n"
#         f"Комментарий: {order.comment or 'Нет'}\n"
#         "Состав заказа:\n"
#     )
#     for product in order.products.all():
#         message += f" - {product.name} (Цена: {product.price})\n"
#
#     try:
#         await bot.send_message(chat_id=settings.TELEGRAM_SUPERADMIN_CHAT_ID, text=message, parse_mode='Markdown')
#     except Exception as e:
#         logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")
#
# def notify_new_order(order):
#     import asyncio
#     asyncio.run(send_order_notification(order))
#
#
# if __name__ == '__main__':
#     print("Telegram бот для уведомлений о заказах запущен.")
