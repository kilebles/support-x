from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    FSInputFile,
)

from settings import SUPPORT_CHAT_ID, IMAGES_DIR


router = Router()


class RequestStates(StatesGroup):
    """FSM states for request handling."""
    waiting_for_request = State()
    waiting_for_response = State()
    waiting_for_user_response = State()


def get_welcome_keyboard() -> InlineKeyboardMarkup:
    """Create welcome keyboard with apply button."""
    button = InlineKeyboardButton(
        text="📝 Оформить заявку",
        callback_data="apply_request"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def get_admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create admin keyboard for request management."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖌 Ответить", callback_data=f"reply_{user_id}")],
        [InlineKeyboardButton(text="❌ Закрыть заявку", callback_data=f"close_{user_id}")]
    ])


def get_user_response_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Create user keyboard for response options."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖌 Ответить", callback_data=f"user_reply_{user_id}")],
        [InlineKeyboardButton(text="❌ Закрыть заявку", callback_data=f"user_close_{user_id}")]
    ])


@router.message(CommandStart())
async def send_welcome(message: Message):
    """Handle /start command - show welcome message with image."""
    username = message.from_user.username or "пользователь"

    welcome_text = (
        f"⚙️ Здравствуйте, {username}! Это бот поддержки.\n"
        "Вы можете оформить заявку, нажав на кнопку ниже."
    )

    # Load image from local file
    photo = FSInputFile(IMAGES_DIR / "main_menu.jpg")

    await message.answer_photo(
        photo=photo,
        caption=welcome_text,
        reply_markup=get_welcome_keyboard()
    )


@router.callback_query(F.data == "apply_request")
async def handle_apply_request(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle apply request button press."""
    await callback_query.answer()
    await state.set_state(RequestStates.waiting_for_request)
    await callback_query.message.answer(
        "Пожалуйста, напишите вашу заявку, и мы обработаем её."
    )


@router.message(RequestStates.waiting_for_request)
async def process_request(message: Message, state: FSMContext):
    """Process user request and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    request_text = message.text

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=f"Новая заявка от {full_name} (ID: {user_id}):\n{request_text}",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_response)
async def block_messages(message: Message):
    """Block messages while request is being processed."""
    await message.answer("Заявка обрабатывается, дождитесь ответа поддержки.")


@router.callback_query(F.data.startswith("reply_"))
async def handle_reply(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle admin reply button press."""
    user_id = int(callback_query.data.split("_")[1])
    await callback_query.answer()

    await callback_query.message.answer("Напишите ваш ответ пользователю.")
    await state.update_data(user_id=user_id)
    await state.set_state(RequestStates.waiting_for_user_response)


@router.message(RequestStates.waiting_for_user_response)
async def process_admin_response(message: Message, state: FSMContext):
    """Process admin response and send to user."""
    data = await state.get_data()
    user_id = data.get("user_id")

    await message.bot.send_message(
        chat_id=user_id,
        text=message.text,
        reply_markup=get_user_response_keyboard(user_id)
    )
    await message.answer("Ответ успешно отправлен пользователю.")

    await state.clear()


@router.callback_query(F.data.startswith("close_"))
async def handle_close_request(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle admin closing request."""
    user_id = int(callback_query.data.split("_")[1])
    await callback_query.answer()

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.bot.send_message(
        chat_id=user_id,
        text="Ваша заявка была закрыта."
    )

    await state.clear()


@router.callback_query(F.data.startswith("user_reply_"))
async def handle_user_reply(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle user reply button press."""
    await callback_query.answer()
    await state.set_state(RequestStates.waiting_for_request)
    await callback_query.message.answer("Пожалуйста, напишите ваш ответ.")


@router.callback_query(F.data.startswith("user_close_"))
async def handle_user_close(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle user closing request."""
    user_id = int(callback_query.data.split("_")[2])
    await callback_query.answer()

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.bot.send_message(
        chat_id=user_id,
        text="Ваша заявка была закрыта."
    )

    await state.clear()


@router.message()
async def block_non_request_messages(message: Message, state: FSMContext):
    """Block any messages when no active request."""
    current_state = await state.get_state()
    if not current_state:
        await message.answer(
            "У вас нет активных заявок. Пожалуйста, создайте заявку через /start."
        )
    else:
        await message.answer("Заявка уже обрабатывается. Дождитесь завершения.")


async def set_commands(bot):
    """Set bot commands."""
    commands = [
        BotCommand(command="start", description="Обратиться в поддержку")
    ]
    await bot.set_my_commands(commands)
