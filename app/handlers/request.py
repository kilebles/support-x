from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
