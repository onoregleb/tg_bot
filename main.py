from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv
from image_processing import remove_background, replace_background
import io

load_dotenv('.env')

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


kb_yes_no = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
    resize_keyboard=True,
    one_time_keyboard=True
)


class ImageProcessingState(StatesGroup):
    waiting_for_replace = State()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Отправьте мне изображение, и я удалю фон.")


@dp.message(lambda message: message.photo)
async def handle_photo(message: Message, state: FSMContext):
    try:
        # Получаем изображение
        photo = message.photo[-1]
        photo_bytes = await bot.download(photo)

        # Удаляем фон
        output_image = remove_background(photo_bytes)
        img_buffer = io.BytesIO()
        output_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        await state.update_data(image_data=img_buffer.getvalue())

        await message.answer_photo(
            BufferedInputFile(img_buffer.getvalue(), filename="no_bg.png"),
            caption="Вот ваше изображение без фона! Хотите заменить фон?",
            reply_markup=kb_yes_no
        )

        # Переключаемся в состояние ожидания ответа
        await state.set_state(ImageProcessingState.waiting_for_replace)

    except Exception as e:
        await message.answer(f"Ошибка при обработке изображения: {str(e)}")


@dp.message(ImageProcessingState.waiting_for_replace, F.text.in_(["Да", "Нет"]))
async def replace_bg_decision(message: Message, state: FSMContext):
    data = await state.get_data()
    image_data = data.get("image_data")

    if message.text == "Да":
        output_image = replace_background(image_data)
        img_buffer = io.BytesIO()
        output_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        await message.answer_photo(
            BufferedInputFile(img_buffer.getvalue(), filename="replaced_bg.png"),
            caption="Вот изображение с замененным фоном!"
        )

    else:
        await message.answer("Окей, оставляем фон прозрачным!")

    await state.clear()  # Завершаем состояние


async def main():
    print("Бот запущен и ждет сообщений!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
