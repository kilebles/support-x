from typing import List, Optional

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo

from app.keyboards import get_admin_keyboard
from app.settings import SUPPORT_CHAT_ID
from app.handlers.states import RequestStates


router = Router()


@router.callback_query(F.data == "apply_request")
async def handle_apply_request(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle apply request button press."""
    await callback_query.answer()
    await state.set_state(RequestStates.waiting_for_request)
    await callback_query.message.answer(
        "Пожалуйста, опишите вашу проблему как можно детальнее, можете приложить фото. Мы поможем вам!"
    )


@router.message(RequestStates.waiting_for_request, F.photo, F.media_group_id)
async def process_request_media_group(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    """Process user request with multiple photos (media group) and send to admins."""
    if not album:
        album = [message]

    user_id = message.from_user.id
    full_name = message.from_user.full_name

    caption_text = ""
    for msg in album:
        if msg.caption:
            caption_text = msg.caption
            break

    await message.answer("Ваша заявка отправлена в поддержку!")

    media = []
    for i, msg in enumerate(album):
        if msg.photo:
            if i == 0:
                media.append(InputMediaPhoto(
                    media=msg.photo[-1].file_id,
                    caption=f"Опять работать... Еще и {len(album)} фоток прислал...\n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{caption_text}</blockquote>"
                ))
            else:
                media.append(InputMediaPhoto(media=msg.photo[-1].file_id))
        elif msg.video:
            if i == 0:
                media.append(InputMediaVideo(
                    media=msg.video.file_id,
                    caption=f"Опять работать... Еще и медиа прислал...\n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{caption_text}</blockquote>"
                ))
            else:
                media.append(InputMediaVideo(media=msg.video.file_id))

    await message.bot.send_media_group(
        chat_id=SUPPORT_CHAT_ID,
        media=media
    )
    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=f"👆 Заявка от {full_name} (ID: <code>{user_id}</code>)",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request, F.photo)
async def process_request_photo(message: Message, state: FSMContext):
    """Process user request with photo and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    caption = message.caption or ""

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_photo(
        chat_id=SUPPORT_CHAT_ID,
        photo=message.photo[-1].file_id,
        caption=f"Опять работать... Еще и фотку прислал...\n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{caption}</blockquote>",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request, F.voice)
async def process_request_voice(message: Message, state: FSMContext):
    """Process user request with voice message and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_voice(
        chat_id=SUPPORT_CHAT_ID,
        voice=message.voice.file_id,
        caption=f"Опять работать... Еще и голосовое прислал...\n{full_name} (ID: <code>{user_id}</code>)",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request, F.video)
async def process_request_video(message: Message, state: FSMContext):
    """Process user request with video and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    caption = message.caption or ""

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_video(
        chat_id=SUPPORT_CHAT_ID,
        video=message.video.file_id,
        caption=f"Опять работать... Еще и видео прислал...\n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{caption}</blockquote>",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request, F.video_note)
async def process_request_video_note(message: Message, state: FSMContext):
    """Process user request with video note (circle video) and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_video_note(
        chat_id=SUPPORT_CHAT_ID,
        video_note=message.video_note.file_id
    )
    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=f"Опять работать... Еще и кружочек прислал...\n{full_name} (ID: <code>{user_id}</code>)",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request, F.document)
async def process_request_document(message: Message, state: FSMContext):
    """Process user request with document and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    caption = message.caption or ""

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_document(
        chat_id=SUPPORT_CHAT_ID,
        document=message.document.file_id,
        caption=f"Опять работать... Еще и документ прислал...\n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{caption}</blockquote>",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_request)
async def process_request(message: Message, state: FSMContext):
    """Process user request and send to admins."""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    request_text = message.text or ""

    await message.answer("Ваша заявка отправлена в поддержку!")

    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=f"Опять работать... \n{full_name} (ID: <code>{user_id}</code>):\n\n<blockquote expandable>{request_text}</blockquote>",
        reply_markup=get_admin_keyboard(user_id)
    )

    await state.set_state(RequestStates.waiting_for_response)


@router.message(RequestStates.waiting_for_response)
async def block_messages(message: Message):
    """Block messages while request is being processed."""
    await message.answer("Заявка обрабатывается, дождитесь ответа поддержки.")


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
