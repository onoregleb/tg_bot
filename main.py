from aiogram import Bot, Dispatcher
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
from image_processing import remove_background
import io

load_dotenv('.env')

# Инициализация бота
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Отправьте мне изображение, и я удалю фон.")


# Обработчик изображений
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    try:
        # Получаем самое большое изображение (последний элемент массива)
        photo = message.photo[-1]

        photo_bytes = await bot.download(photo)

        output_image = remove_background(photo_bytes)
        img_buffer = io.BytesIO()
        output_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        await message.answer_photo(
            BufferedInputFile(img_buffer.getvalue(), filename="no_bg.png"),
            caption="Вот ваше изображение без фона!"
        )

    except Exception as e:
        await message.answer(f"Ошибка при обработке изображения: {str(e)}")


async def main():
    print("Бот запущен и ждет сообщений!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    # Запуск бота
    asyncio.run(main())
