import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен бота из переменных Railway
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот запущен и работает 24/7 ✅\n\n"
        "Используй команду:\n"
        "/s <название>"
    )

@bot.message_handler(commands=["s"])
def search_script(message):
    query = message.text.replace("/s", "").strip()

    if not query:
        bot.send_message(
            message.chat.id,
            "❌ Укажи запрос\n\nПример:\n/s evade"
        )
        return

    # 🔗 пример ссылки (потом заменишь на реальный поиск)
    lua_url = "https://rawscripts.net/raw/Random-Mafia-Shooter-esp-aimbot-noclip-97624"

    script_message = (
        f"🔍 Поиск по запросу: *{query}*\n\n"
        "```lua\n"
        f'loadstring(game:HttpGet("{lua_url}"))()\n'
        "```"
    )

    bot.send_message(
        message.chat.id,
        script_message,
        parse_mode="Markdown"
    )

print("Bot is running...")
bot.infinity_polling()
