import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from google import genai

TOKEN = "8660484025:AAEUY9uyq-p0vChG-EFtD0oycsjiN_x0SMc"

client = genai.Client()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer(
      f"Привет, {html.bold(message.from_user.full_name)}! Отправь мне"
      " математическую задачу или пример, и я помогу её решить."
  )


@dp.message()
async def solve_math_handler(message: Message) -> None:
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Ты — опытный учитель математики. Подробно и понятно реши следующую"
            f" задачу или пример: {message.text}"
        ),
    )
    await message.answer(response.text)
  except Exception as e:
    await message.answer(
        "Произошла ошибка при обработке запроса. Попробуй еще раз."
    )


async def main() -> None:
  bot = Bot(
      token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
  )
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())

