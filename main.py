import telebot
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "findscripts-bot"
}

def find_lua_files(contents_url):
    r = requests.get(contents_url, headers=HEADERS)
    if r.status_code != 200:
        return []

    results = []
    items = r.json()

    if not isinstance(items, list):
        return []

    for item in items:
        if item["type"] == "file" and item["name"].endswith(".lua"):
            results.append(item["download_url"])

        if item["type"] == "dir":
            sub = requests.get(item["url"], headers=HEADERS)
            if sub.status_code != 200:
                continue
            for f in sub.json():
                if f["type"] == "file" and f["name"].endswith(".lua"):
                    results.append(f["download_url"])

    return results


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Бот работает\n\n"
        "Команда:\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 2"
    )


@bot.message_handler(commands=["s"])
def search(message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        bot.reply_to(message, "❌ /s <запрос> <кол-во>")
        return

    query = args[1]
    try:
        limit = int(args[2])
    except:
        bot.reply_to(message, "❌ Кол-во должно быть числом")
        return

    search_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} roblox script",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    r = requests.get(search_url, params=params, headers=HEADERS)
    if r.status_code != 200:
        bot.send_message(message.chat.id, "❌ Ошибка GitHub API")
        return

    repos = r.json().get("items", [])
    found = 0

    bot.send_message(message.chat.id, f"🔍 Поиск по запросу: {query}")

    for repo in repos:
        if found >= limit:
            break

        contents_url = repo["contents_url"].replace("{+path}", "")
        lua_files = find_lua_files(contents_url)

        for raw in lua_files:
            bot.send_message(
                message.chat.id,
                f"```lua\nloadstring(game:HttpGet(\"{raw}\"))()\n```",
                parse_mode="Markdown"
            )
            found += 1
            break

    if found == 0:
        bot.send_message(message.chat.id, "❌ Lua-скрипты не найдены")


bot.infinity_polling()
