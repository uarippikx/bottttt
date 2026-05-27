from aiogram.fsm.state import State, StatesGroup

class Regestration(StatesGroup):
    waiting_email = State()
    waiting_password = State()