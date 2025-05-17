from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

categories = ["🎬 Movies", "🎮 Games", "📺 TV Shows", "📚 Books", "🎌 Anime"]

category_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=category)] for category in categories],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔙 Back to Main Menu")]],
    resize_keyboard=True
)

more_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="More recommendations", callback_data="more")]]
)

combined_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Back to Main Menu"), KeyboardButton(text="/random")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Enter title or genre..."
)
