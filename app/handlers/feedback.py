from typing import List, Optional

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo

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


@router.message(FeedbackStates.waiting_for_feedback, F.photo, F.media_group_id)
async def process_feedback_media_group(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    """Process user feedback with multiple photos (media group) and send to admins."""
    if not album:
        album = [message]

    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"

    caption_text = ""
    for msg in album:
        if msg.caption:
            caption_text = msg.caption
            break

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    media = []
    for i, msg in enumerate(album):
        if msg.photo:
            if i == 0:
                media.append(InputMediaPhoto(
                    media=msg.photo[-1].file_id,
                    caption=(
                        f"💬 Новый отзыв ({len(album)} фото)\n\n"
                        f"От: {full_name}\n"
                        f"Username: @{username}\n"
                        f"ID: {user_id}\n\n"
                        f"Отзыв:\n{caption_text}"
                    )
                ))
            else:
                media.append(InputMediaPhoto(media=msg.photo[-1].file_id))
        elif msg.video:
            if i == 0:
                media.append(InputMediaVideo(
                    media=msg.video.file_id,
                    caption=(
                        f"💬 Новый отзыв (медиа)\n\n"
                        f"От: {full_name}\n"
                        f"Username: @{username}\n"
                        f"ID: {user_id}\n\n"
                        f"Отзыв:\n{caption_text}"
                    )
                ))
            else:
                media.append(InputMediaVideo(media=msg.video.file_id))

    await message.bot.send_media_group(
        chat_id=FEEDBACK_CHAT_ID,
        media=media
    )

    await state.clear()


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


@router.message(FeedbackStates.waiting_for_feedback, F.voice)
async def process_feedback_voice(message: Message, state: FSMContext):
    """Process user feedback with voice message and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_voice(
        chat_id=FEEDBACK_CHAT_ID,
        voice=message.voice.file_id,
        caption=(
            f"💬 Новый отзыв (голосовое)\n\n"
            f"От: {full_name}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}"
        )
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_feedback, F.video)
async def process_feedback_video(message: Message, state: FSMContext):
    """Process user feedback with video and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"
    feedback_text = message.caption or ""

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_video(
        chat_id=FEEDBACK_CHAT_ID,
        video=message.video.file_id,
        caption=(
            f"💬 Новый отзыв (видео)\n\n"
            f"От: {full_name}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}\n\n"
            f"Отзыв:\n{feedback_text}"
        )
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_feedback, F.video_note)
async def process_feedback_video_note(message: Message, state: FSMContext):
    """Process user feedback with video note and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_video_note(
        chat_id=FEEDBACK_CHAT_ID,
        video_note=message.video_note.file_id
    )
    await message.bot.send_message(
        chat_id=FEEDBACK_CHAT_ID,
        text=(
            f"💬 Новый отзыв (кружочек)\n\n"
            f"От: {full_name}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}"
        )
    )

    await state.clear()


@router.message(FeedbackStates.waiting_for_feedback, F.document)
async def process_feedback_document(message: Message, state: FSMContext):
    """Process user feedback with document and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username or "не указан"
    feedback_text = message.caption or ""

    await message.answer("Спасибо за ваш отзыв! Мы обязательно его рассмотрим.")

    await message.bot.send_document(
        chat_id=FEEDBACK_CHAT_ID,
        document=message.document.file_id,
        caption=(
            f"💬 Новый отзыв (документ)\n\n"
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
