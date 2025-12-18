from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.keyboards import get_user_response_keyboard
from app.handlers.states import RequestStates


router = Router()


@router.callback_query(F.data.startswith("reply_"))
async def handle_reply(callback_query: CallbackQuery, state: FSMContext):
    """Handle admin reply button press."""
    user_id = int(callback_query.data.split("_")[1])
    await callback_query.answer()

    await callback_query.message.answer("Напишите ваш ответ пользователю.")
    await state.update_data(user_id=user_id)
    await state.set_state(RequestStates.waiting_for_user_response)


@router.message(RequestStates.waiting_for_user_response, F.photo)
async def process_admin_response_photo(message: Message, state: FSMContext):
    """Process admin response with photo and send to user."""
    data = await state.get_data()
    user_id = data.get("user_id")

    await message.bot.send_photo(
        chat_id=user_id,
        photo=message.photo[-1].file_id,
        caption=message.caption,
        reply_markup=get_user_response_keyboard(user_id)
    )
    await message.answer("Ответ успешно отправлен пользователю.")

    await state.clear()


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
async def handle_close_request(callback_query: CallbackQuery, state: FSMContext):
    """Handle admin closing request."""
    user_id = int(callback_query.data.split("_")[1])
    await callback_query.answer()

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.bot.send_message(
        chat_id=user_id,
        text="Ваша заявка была закрыта."
    )

    await state.clear()
