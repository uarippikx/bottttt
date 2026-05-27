from aiogram.fsm.state import State, StatesGroup

class Profile(StatesGroup):
    changing_email = State()