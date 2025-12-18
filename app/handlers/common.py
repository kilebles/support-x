from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


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
