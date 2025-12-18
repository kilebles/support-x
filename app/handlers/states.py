from aiogram.fsm.state import State, StatesGroup


class RequestStates(StatesGroup):
    """FSM states for request handling."""
    waiting_for_request = State()
    waiting_for_response = State()
    waiting_for_user_response = State()


class FeedbackStates(StatesGroup):
    """FSM states for feedback handling."""
    waiting_for_feedback = State()
