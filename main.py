import telebot
import requests
import os
import re

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "findscripts-bot"
}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 FindScripts бот\n\n"
        "Команда:\n"
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

    search_url = "https://api.github.com/search/code"
    params = {
        "q": f'{query} loadstring(game:HttpGet language:Lua',
        "per_page": min(limit * 3, 30)
    }

    r = requests.get(search_url, headers=HEADERS, params=params)
    if r.status_code != 200:
        bot.send_message(message.chat.id, "❌ Ошибка GitHub API")
        return

    results = r.json().get("items", [])
    found = 0

    for item in results:
        if found >= limit:
            break

        raw_url = item["html_url"].replace(
            "https://github.com/",
            "https://raw.githubusercontent.com/"
        ).replace("/blob/", "/")

        file = requests.get(raw_url)
        if file.status_code != 200:
            continue

        matches = re.findall(
            r'loadstring\(game:HttpGet\(["\'](.*?)["\']\)\)\(\)',
            file.text
        )

        for m in matches:
            bot.send_message(
                message.chat.id,
                f"```lua\nloadstring(game:HttpGet(\"{m}\"))()\n```",
                parse_mode="Markdown"
            )
            found += 1
            break

    if found == 0:
        bot.send_message(message.chat.id, "❌ Lua-скрипты не найдены")


bot.infinity_polling()
