from aiogram import types
from aiogram.filters import Command
import re
from bot.keyboards import category_keyboard, more_keyboard, combined_keyboard
from bot.data import user_states, categories, category_names, random_prompts
from bot.services.gemini import get_gemini_recommendations
from bot.bot_instance import bot, dp


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle the /start command."""
    await message.answer("Welcome to RecQuest! Choose a category:", reply_markup=category_keyboard)
    user_id = message.from_user.id
    user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    """Handle the /random command."""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        await message.answer("Please choose a category first:", reply_markup=category_keyboard)
        user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}
        return
    
    state = user_states[user_id]
    
    if "category" not in state:
        await message.answer("Please choose a category first:", reply_markup=category_keyboard)
        state["step"] = "choose_category"
        return
    
    # Get a random prompt for the selected category
    category = state["category"]
    prompts = random_prompts.get(category, [f"popular {category_names.get(category, 'item')}"])
    random_prompt = random.choice(prompts)
    
    # Show loading message
    loading_message = await message.answer(f"Finding a random {category_names.get(category, category.lower())} recommendation...")
    
    # Get recommendation
    state["query"] = random_prompt  # Save the query for "More" button
    state["previous_recommendations"] = set()  # Reset previous recommendations
    recommendations = await get_gemini_recommendations(category, random_prompt, state["previous_recommendations"])
    
    # Update previous recommendations
    for rec in recommendations:
        title_match = re.match(r'^\d+\.\s+([^-]+)\s+-', rec)
        if title_match:
            state["previous_recommendations"].add(title_match.group(1).strip())
    
    # Delete loading message and send recommendations
    await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
    await message.answer(f"Random {category_names.get(category, category.lower())} recommendations:", reply_markup=more_keyboard)
    await message.answer("\n".join(recommendations))
    await message.answer("Need something else?", reply_markup=combined_keyboard)

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Handle back to main menu command
    if text == "🔙 Back to Main Menu":
        await message.answer("Choose a category:", reply_markup=category_keyboard)
        user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}
        return
        
    # Handle /random command through keyboard
    if text == "/random":
        # Create a fake message for the command handler
        fake_message = types.Message(
            message_id=message.message_id,
            date=message.date,
            chat=message.chat,
            from_user=message.from_user,
            content_type=message.content_type,
            text="/random"
        )
        await cmd_random(fake_message)
        return

    if user_id not in user_states:
        await message.answer("Choose a category:", reply_markup=category_keyboard)
        user_states[user_id] = {"step": "choose_category", "previous_recommendations": set()}
        return

    state = user_states[user_id]

    if state["step"] == "choose_category":
        if text in categories:
            state["category"] = text
            state["step"] = "ask_query"
            # Use the clean category name from the mapping
            category_name = category_names.get(text, text.lower().replace("🎬 ", "").replace("🎮 ", "").replace("📺 ", "").replace("📚 ", "").replace("🎌 ", ""))
            await message.answer(f"Enter a {category_name} title or genre:", reply_markup=combined_keyboard)
        else:
            await message.answer("Please select a category from the keyboard.")

    elif state["step"] == "ask_query":
        state["query"] = text
        state["step"] = "recommendations"
        state["previous_recommendations"] = set()  # Reset previous recommendations
        
        # Show loading message
        loading_message = await message.answer("Searching for recommendations...")
        
        recommendations = await get_gemini_recommendations(state["category"], text, state["previous_recommendations"])
        
        # Update previous recommendations
        for rec in recommendations:
            title_match = re.match(r'^\d+\.\s+([^-]+)\s+-', rec)
            if title_match:
                state["previous_recommendations"].add(title_match.group(1).strip())
        
        # Delete loading message and send recommendations
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
        await message.answer("\n".join(recommendations), reply_markup=more_keyboard)
        # Keep the back button available
        await message.answer("Need something else?", reply_markup=combined_keyboard)