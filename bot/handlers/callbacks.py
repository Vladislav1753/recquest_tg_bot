import re
from aiogram import types
from bot.keyboards.keyboards import category_keyboard, more_keyboard
from bot.data.user_states import user_states
from bot.services.gemini import get_gemini_recommendations

async def handle_more_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_states:
        await callback_query.message.answer("Session expired. Please start over:", reply_markup=category_keyboard)
        user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}
        await callback_query.answer()
        return

    state = user_states[user_id]

    if "category" in state and "query" in state:
        loading_message = await callback_query.message.answer("Searching for more recommendations...")

        recommendations = await get_gemini_recommendations(state["category"], state["query"], state["previous_recommendations"])

        for rec in recommendations:
            title_match = re.match(r'^\d+\.\s+([^-]+)\s+-', rec)
            if title_match:
                state["previous_recommendations"].add(title_match.group(1).strip())

        await callback_query.message.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=loading_message.message_id)
        await callback_query.message.answer("\n".join(recommendations), reply_markup=more_keyboard)
    else:
        await callback_query.message.answer("Something went wrong. Please start over:", reply_markup=category_keyboard)
        user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}

    await callback_query.answer()