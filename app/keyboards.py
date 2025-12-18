from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_welcome_keyboard() -> InlineKeyboardMarkup:
    """Create welcome keyboard with apply and feedback buttons."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 Оформить заявку",
            callback_data="apply_request"
        )],
        [InlineKeyboardButton(
            text="💬 Отправить отзыв",
            callback_data="send_feedback"
        )]
    ])


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
