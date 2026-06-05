from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers.reg import cmd_reg, email, password
from handlers.profile import profile_cmd, email_change, new_email

from FSM.regFSM import Regestration
from FSM.profileFSM import Profile
from middlewares.middleware import Registration_MW

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.middleware(Registration_MW())
dp.callback_query.middleware(Registration_MW())
    
dp.message.register(cmd_reg, Command("start"))
dp.message.register(profile_cmd, Command("profile"))
dp.message.register(email_change, Command("email"))

dp.message.register(email,StateFilter(Regestration.waiting_email))
dp.message.register(password,StateFilter(Regestration.waiting_password))
dp.message.register(new_email, StateFilter(Profile.changing_email))


async def main():               
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())