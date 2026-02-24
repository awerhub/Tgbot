import telebot
import requests
import os

# === НАСТРОЙКИ ===
TOKEN = os.getenv("BOT_TOKEN")  # токен бота (обязательно в Railway Variables)
bot = telebot.TeleBot(TOKEN)

# === /start ===
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Бот запущен и работает 24/7 ✅\n\n"
        "Команда поиска:\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 2"
    )

# === /s поиск ===
@bot.message_handler(func=lambda m: m.text and m.text.startswith("/s"))
def search(message):
    args = message.text.split(maxsplit=2)

    if len(args) < 2:
        bot.reply_to(message, "❗ Пример: /s evade 2")
        return

    query = args[1]
    count = 1

    if len(args) == 3 and args[2].isdigit():
        count = int(args[2])

    url = f"https://api.github.com/search/repositories?q={query}+roblox+script"
    headers = {"Accept": "application/vnd.github+json"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
    except Exception:
        bot.reply_to(message, "❌ Ошибка при запросе к GitHub")
        return

    if "items" not in data or len(data["items"]) == 0:
        bot.reply_to(message, "❌ Ничего не найдено")
        return

    msg = "🔍 Найденные репозитории:\n\n"
    for repo in data["items"][:count]:
        msg += (
            f"📦 {repo['full_name']}\n"
            f"⭐ Stars: {repo['stargazers_count']}\n"
            f"🔗 {repo['html_url']}\n\n"
        )

    bot.reply_to(message, msg)

# === ЗАПУСК ===
print("Bot is running...")
bot.infinity_polling()
