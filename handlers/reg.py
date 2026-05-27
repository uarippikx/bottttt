from FSM.regFSM import Regestration
from Connections.postgresql import pg_manager as manager

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ContentType
from aiogram import types

def is_valid_email(email:str):
    dog = email.find("@")
    return (dog != -1 and email.count("@") == 1) and ("a" in email [dog+1:])

async def cmd_reg(message:types.Message, state: FSMContext): #асинхронная функция запускается если срабатывает верхнее условие
    await state.set_state(Regestration.waiting_email)
    await message.answer("Введи почту:")

async def email(message:types.Message, state:FSMContext):
    if not is_valid_email(message.text):
        await message.answer("Некорректная почта")
        return
    await state.update_data(email = message.text)
    await message.answer("Введи пароль")
    await state.set_state(Regestration.waiting_password)

async def password(message:Message, state:FSMContext):
    passw = message.text
    user = await state.get_data()
    async with manager:
        await manager.insert_data_with_update(
            table_name="usersdata",
            records_data={
                "user_id":message.from_user.id,
                "username":message.from_user.username,
                "email":user.get("email"),
                "password":passw},
            conflict_column="user_id")
    await state.clear()
    await message.answer("Ты успешно зарегистрировался!")