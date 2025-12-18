from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.settings import FEEDBACK_CHAT_ID
from app.handlers.states import FeedbackStates


router = Router()


@router.callback_query(F.data == "send_feedback")
async def handle_send_feedback(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle send feedback button press."""
    await callback_query.answer()
    await state.set_state(FeedbackStates.waiting_for_feedback)
    await callback_query.message.answer(
        "Пожалуйста, напишите ваш отзыв. Мы ценим ваше мнение!"
    )


@router.message(FeedbackStates.waiting_for_feedback, F.photo)
async def process_feedback_photo(message: Message, state: FSMContext):
    """Process user feedback with photo and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"
    feedback_text = message.caption or ""

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_photo(
        chat_id=FEEDBACK_CHAT_ID,
        photo=message.photo[-1].file_id,
        caption=(
            f"💬 Новый отзыв\n\n"
            f"От: {full_name}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}\n\n"
            f"Отзыв:\n{feedback_text}"
        )
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    """Process user feedback and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"
    feedback_text = message.text or ""

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_message(
        chat_id=FEEDBACK_CHAT_ID,
        text=(
            f"💬 Новый отзыв\n\n"
            f"От: {full_name}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}\n\n"
            f"Отзыв:\n{feedback_text}"
        )
    )

    await state.clear()
