import telebot
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")  # обязательно через env
bot = telebot.TeleBot(TOKEN)

GITHUB_SEARCH = "https://api.github.com/search/repositories"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "findscripts-bot"
}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот запущен и работает 24/7 ✅\n\n"
        "Команда поиска:\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 2"
    )

@bot.message_handler(commands=["s"])
def search_scripts(message):
    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        bot.reply_to(message, "❌ Используй:\n/s <запрос> <кол-во>")
        return

    query = args[1]
    try:
        limit = int(args[2])
    except ValueError:
        bot.reply_to(message, "❌ Кол-во должно быть числом")
        return

    params = {
        "q": f"{query} roblox script",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    r = requests.get(GITHUB_SEARCH, params=params, headers=GITHUB_HEADERS)
    if r.status_code != 200:
        bot.reply_to(message, "❌ Ошибка GitHub API")
        return

    repos = r.json().get("items", [])
    if not repos:
        bot.reply_to(message, "❌ Ничего не найдено")
        return

    found = 0
    bot.send_message(message.chat.id, f"🔍 Поиск по запросу: {query}")

    for repo in repos:
        if found >= limit:
            break

        owner = repo["owner"]["login"]
        name = repo["name"]
        contents_url = f"https://api.github.com/repos/{owner}/{name}/contents"

        c = requests.get(contents_url, headers=GITHUB_HEADERS)
        if c.status_code != 200:
            continue

        files = c.json()
        if not isinstance(files, list):
            continue

        for f in files:
            if f["type"] == "file" and f["name"].endswith(".lua"):
                raw_url = f["download_url"]

                bot.send_message(
                    message.chat.id,
                    f"```lua\n"
                    f"loadstring(game:HttpGet(\"{raw_url}\"))()\n"
                    f"```",
                    parse_mode="Markdown"
                )

                found += 1
                break  # берём ОДИН lua из репо

    if found == 0:
        bot.send_message(message.chat.id, "❌ Lua-скрипты не найдены")

print("Bot started")
bot.infinity_polling()
