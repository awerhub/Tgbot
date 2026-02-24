import telebot
import requests
import os

TOKEN = os.getenv("BOT_TOKEN") or "7660869244:AAHEbtO0AXrAlJD85smlXGskC203pfuLqec"
bot = telebot.TeleBot(TOKEN)

GITHUB_API = "https://api.github.com/search/code"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "tg-bot"
}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот запущен\n\n"
        "Команда:\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 1"
    )

@bot.message_handler(commands=["s"])
def search(message):
    args = message.text.split()

    if len(args) < 3:
        bot.send_message(message.chat.id, "❌ Используй: /s <запрос> <кол-во>")
        return

    query = args[1]

    try:
        limit = int(args[2])
    except ValueError:
        bot.send_message(message.chat.id, "❌ Кол-во должно быть числом")
        return

    bot.send_message(message.chat.id, f"🔍 Поиск по запросу: {query}")

    params = {
        "q": query,
        "per_page": min(limit, 30)
    }

    r = requests.get(GITHUB_API, headers=HEADERS, params=params)

    if r.status_code != 200:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка GitHub API ({r.status_code})"
        )
        return

    items = r.json().get("items", [])

    if not items:
        bot.send_message(message.chat.id, "❌ Ничего не найдено")
        return

    sent = 0
    for item in items:
        if sent >= limit:
            break

        url = item.get("html_url")
        if url:
            bot.send_message(message.chat.id, url)
            sent += 1

bot.infinity_polling()
