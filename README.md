# RecQuest — Telegram Bot

Welcome to my small pet-project — RecQuest!

TG username of RecQuest — @recquest_bot.

RecQuest is a Telegram bot that recommends **movies**, **TV shows**, **games**, **books**, and **anime** using Google's **Gemini API** (LLM).

## 🎯 Features

- Interactive Telegram bot interface
- Categories: 🎬 Movies, 📺 TV Shows, 🎮 Games, 📚 Books, 🎌 Anime
- Personalized recommendations based on user queries
- `/random` command to get surprise suggestions
- Inline buttons for "More" or going back to main menu
- State tracking per user session

## 🛠 Tech Stack

- Python
- Aiogram (Telegram Bot API)
- Google Gemini API
- Railway (deployment)
- dotenv (for environment variables)


## 📦 Installation

```
git clone https://github.com/yourusername/recquest_tg_bot.git
cd recquest_tg_bot
pip install -r requirements.txt
python bot/main.py
````

## 📁 Project Structure


```
bot/
├── data/
│   ├── constants.py
│   ├── prompts.py
│   └── user_states.py
├── handlers/
│   ├── callbacks.py
│   ├── handlers.py
│   ├── start.py
│   └── user.py
├── keyboards/
│   └── keyboards.py
├── services/
│   ├── gemini.py
├── utils/
│   └── helpers.py
├── bot_instance.py
└── main.py
```

## ⚙️ Environment Variables

Create a `.env` file with the following:

```
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```


## 🚀 Deployment

The bot is currently deployed on **Railway**.
To deploy your own instance, push your code to GitHub and connect it to Railway.

## 📸 Demo
![image](https://github.com/user-attachments/assets/1df0a841-7f51-45f3-b215-6e2eeb7ca590)
