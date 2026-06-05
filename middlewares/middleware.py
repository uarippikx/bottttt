from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from FSM.regFSM import Regestration
from aiogram.types import TelegramObject, Message, CallbackQuery
from Connections.postgresql import pg_manager as manager

class Registration_MW(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any: 
        user_id=None
        text=''
        if isinstance(event,Message):
            user_id=event.from_user.id
            text=event.text or ""
        elif isinstance(event, CallbackQuery):
            user_id=event.from_user.id
            text=event.data or ""
        else:
            return await handler(event,data)
        state=data.get('state')
        current_state=None
        if state:
            current_state= await state.get_state()
        allowed=['/start','/help','/email']
        if isinstance(event,Message):
            if any(text.startswith(cmd) for cmd in allowed):
                return await handler(event,data)
            reg_states=[Regestration.waiting_email.state, Regestration.waiting_password.state]
        if current_state in reg_states:
                return await handler(event,data)
           
        async with manager:
            user = await manager.select_data(
                table_name="userssdata",
                where_dict={
                    "user_id" : user_id
                },
                one_dict=True
            )
        if not user:
            await event.answer('Ты не зареган')
        
        return await handler(event,data)