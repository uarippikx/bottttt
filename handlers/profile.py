from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ContentType
from aiogram import types
from Connections.postgresql import pg_manager as manager
from FSM.profileFSM import Profile
from handlers.reg import is_valid_email

async def profile_cmd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with manager:
        user = await manager.select_data(
            table_name="usersdata",
            where_dict={
                "user_id" : user_id
            },
            one_dict=True
        )
    if not user:
        await message.answer("Ты не зареган!")
        return
    text = (
        "<b>Ваш профиль </b>\n"
        f"ID <code>{user_id}</code>\n"
        f"Имя {user.get('username')}\n"
        f"Почта {user.get('email')}"
    )

    button = KeyboardButton(text="/email")
    kb = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    await message.answer(text, parse_mode="HTML", reply_markup=kb)

async def email_change(message: types.Message, state: FSMContext):
    await message.answer("Введи новую почту:")
    await state.set_state(Profile.changing_email)

async def new_email(message:types.Message, state:FSMContext):
    if not is_valid_email(message.text):
        await message.answer("Некорректная почта")
        return
    async with manager:
        manager.update_data(
            table_name="usersdata",
            where_dict={
                "user_id" : message.from_user.id
            },
            update_dict={
                "email" : message.text
            }
        )

        
    await message.answer("Вы поменяли почту!")
    await state.clear()
    