from aiogram import types, Router
from aiogram.filters import Command
from bot.keyboards.keyboards import category_keyboard
from bot.data.user_states import user_states

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the Recommendation Bot! Choose a category:", reply_markup=category_keyboard)
    user_id = message.from_user.id
    user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}
