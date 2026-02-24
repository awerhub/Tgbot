import telebot
import requests
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "User-Agent": "findscripts-bot"
}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 FindScripts бот\n\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 1"
    )


@bot.message_handler(commands=["s"])
def search(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "❌ /s <запрос> <кол-во>")
        return

    query = args[1]
    try:
        limit = int(args[2])
    except:
        bot.reply_to(message, "❌ Кол-во должно быть числом")
        return

    bot.send_message(message.chat.id, f"🔍 Поиск по запросу: {query}")

    url = "https://api.github.com/search/code"
    params = {
        "q": f'{query} loadstring(game:HttpGet',
        "per_page": 30
    }

    r = requests.get(url, headers=HEADERS, params=params)

    if r.status_code != 200:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка GitHub API ({r.status_code})"
        )
        return

    items = r.json().get("items", [])
    found = 0

    for item in items:
        if found >= limit:
            break

        raw = item["html_url"] \
            .replace("https://github.com/", "https://raw.githubusercontent.com/") \
            .replace("/blob/", "/")

        file = requests.get(raw)
        if file.status_code != 200:
            continue

        matches = re.findall(
            r'loadstringgame:HttpGet\(["\'](.*?)["\']\)',
            file.text
        )

        for m in matches:
            bot.send_message(
                message.chat,Id,
                m 
)
