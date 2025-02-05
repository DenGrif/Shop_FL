# bot/telegram_bot.py
import os
import logging
from telegram import Bot
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI', settings.TELEGRAM_BOT_TOKEN)
TELEGRAM_SUPERADMIN_CHAT_ID = os.environ.get('1375390614', settings.TELEGRAM_SUPERADMIN_CHAT_ID)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def notify_new_order(order):
    message = (
        f"*Новый заказ* №{order.pk}\n"
        f"Пользователь: {order.user.username}\n"
        f"Сумма заказа: {order.total_price}\n"
        f"Дата доставки: {order.delivery_date}\n"
        f"Время доставки: {order.delivery_time}\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Комментарий: {order.comment or 'Нет'}\n"
        "Состав заказа:\n"
    )
    for product in order.products.all():
        message += f" - {product.name} (Цена: {product.price})\n"

    try:
        bot.send_message(chat_id=TELEGRAM_SUPERADMIN_CHAT_ID, text=message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")

if __name__ == '__main__':
    print("Telegram бот для уведомлений о заказах запущен.")


