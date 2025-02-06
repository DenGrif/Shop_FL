# bot/telegram_bot.py
import os
import django
import asyncio
import threading
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from django.conf import settings
from asgiref.sync import sync_to_async

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flshop.settings')
# Инициализируем Django
django.setup()

# Импортируем модель Order после инициализации Django
from shop.models import Order

# Используем настройки из settings.py
API_TOKEN = settings.TELEGRAM_BOT_TOKEN  # '8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI'
TELEGRAM_CHAT_ID = settings.TELEGRAM_SUPERADMIN_CHAT_ID  # '1375390614'

# Инициализация бота и диспетчера (aiogram 2.x)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Асинхронная функция для отправки уведомления о новом заказе
async def send_order_notification(order):
    logging.info(f"[DEBUG] Запущена send_order_notification для заказа {order.id}")

    # Формируем сообщение для отправки
    message = f"*Новый заказ* №{order.id} от пользователя {order.user.username}\n"
    message += f"Дата заказа: {order.created_at}\n"
    message += "Продукты в заказе:\n"

    # Безопасно получаем список товаров через sync_to_async
    products = await sync_to_async(list)(order.products.all())
    logging.info(f"[DEBUG] Найдено продуктов: {len(products)}")

    for product in products:
        qty = getattr(product, 'quantity', 1)
        total_price = product.price * qty
        message += f"- {product.name} (x{qty}) - {total_price} ₽\n"

    message += f"\nОбщая сумма заказа: {order.total_price} ₽"
    logging.info(f"[DEBUG] Отправка сообщения: {message}")

    try:
        await bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode=ParseMode.MARKDOWN)
        logging.info("[DEBUG] Сообщение успешно отправлено")
    except Exception as e:
        logging.error(f"[ERROR] Ошибка при отправке сообщения: {e}")


# Функция для вызова уведомления о новом заказе в отдельном потоке
def notify_new_order(order):
    logging.info(f"[DEBUG] notify_new_order вызвана для заказа {order.id}")

    def run():
        # Создаем новый цикл событий для данного потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(send_order_notification(order))
        except Exception as e:
            logging.error(f"[ERROR] Ошибка в notify_new_order: {e}")
        finally:
            loop.close()

    # Запускаем новый поток, который выполнит функцию run()
    threading.Thread(target=run).start()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в магазин!")


# Обработчик команды /new_order для тестирования уведомления
@dp.message_handler(commands=['new_order'])
async def new_order(message: types.Message):
    # Пример: берем заказ с ID=1 (замените на актуальный ID заказа)
    order = Order.objects.get(id=1)
    notify_new_order(order)
    await message.answer(f"Уведомление о заказе {order.id} отправлено.")


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
