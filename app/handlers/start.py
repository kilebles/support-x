from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BotCommand

from app.keyboards import get_welcome_keyboard
from app.settings import IMAGES_DIR


router = Router()


@router.message(CommandStart())
async def send_welcome(message: Message):
    """Handle /start command - show welcome message with image."""
    username = message.from_user.username or "пользователь"

    welcome_text = (
        f"⚙️ Здравствуйте, {username}! Это бот поддержки.\n"
        "Вы можете обратиться в поддержку или оставить отзыв, нажав на кнопки ниже."
    )

    photo = FSInputFile(IMAGES_DIR / "main_menu.jpg")

    await message.answer_photo(
        photo=photo,
        caption=welcome_text,
        reply_markup=get_welcome_keyboard()
    )


async def set_commands(bot):
    """Set bot commands."""
    commands = [
        BotCommand(command="start", description="Обратиться в поддержку")
    ]
    await bot.set_my_commands(commands)
