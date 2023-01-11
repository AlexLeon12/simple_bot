"""
simple telegram-bot

python-3.8.6
python main.py
"""

import os
import logging
from urllib.parse import urljoin

from aiogram import Bot, executor
from aiogram.types import Message, ContentTypes
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


MODE = os.getenv("MODE", "dev")
# MODE = os.getenv("MODE", "prod")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# ---webhook settings
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/")
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_PATH)

# ---webserver settings
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
# WEBAPP_HOST = os.getenv("WEBAPP_HOST", "127.0.0.1")
WEBAPP_PORT = int(os.getenv("PORT", 80))

ADMIN_ID = int(os.getenv("ADMIN_ID"))


print("WEBHOOK_URL", type(WEBHOOK_URL), WEBHOOK_URL)
print("WEBAPP_HOST", type(WEBAPP_HOST), WEBAPP_HOST)
print("WEBAPP_PORT", type(WEBAPP_PORT), WEBAPP_PORT)
print("ADMIN_ID", type(ADMIN_ID), ADMIN_ID)
print("API_TOKEN", type(API_TOKEN), API_TOKEN)


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(msg: Message):
	# Regular request
	# await bot.send_message(msg.chat.id, msg.text)
	_id = msg.chat.id
	print(type(_id), _id)

	await msg.answer(f"echo: {msg.text}")

	await bot.send_message(ADMIN_ID, f"recieved: {msg.text}")

	# or reply INTO webhook
	# return SendMessage(msg.chat.id, msg.text)
	# return SendMessage(msg.chat.id, msg.text)

# @dp.message_handler()
# async def default_handler(msg):
# 	print("default_handler", msg)
# 	# await msg.answer("view help")
# 	await bot.send_message(ADMIN_ID, f"recieved: {msg}")


async def on_startup(dp):
	print("on_startup")
	await bot.delete_webhook()
	await bot.set_webhook(WEBHOOK_URL)
	# insert code here to run it after start


async def on_shutdown(dp):
	print("on_shutdown")
	logging.warning('Shutting down..')

	# await bot.send_message(ADMIN_ID, "Shutting down..")

	# insert code here to run it before shutdown

	# Close DB connection (if used)
	await dp.storage.close()
	await dp.storage.wait_closed()

	logging.warning('Bye!')




if __name__ == "__main__":
	# HTTP_PROXY / HTTPS_PROXY environment

	HTTP_PROXY = os.getenv("HTTP_PROXY")
	HTTPS_PROXY = os.getenv("HTTPS_PROXY")
	print(f"HTTP_PROXY: {HTTP_PROXY}")
	print(f"HTTPS_PROXY: {HTTPS_PROXY}")

	if MODE == "dev":
		executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)
	else:
		start_webhook(
			dispatcher=dp,
			webhook_path=WEBHOOK_PATH,
			on_startup=on_startup,
			on_shutdown=on_shutdown,
			skip_updates=True,
			host=WEBAPP_HOST,
			port=WEBAPP_PORT,
		)