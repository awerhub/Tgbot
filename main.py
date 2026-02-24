import telebot
import requests

TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SEARCH_API = "https://api.github.com/search/repositories"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот работает ✅\n\n"
        "Поиск:\n"
        "/s <запрос> <кол-во>\n\n"
        "Пример:\n"
        "/s evade 2"
    )

@bot.message_handler(commands=["s"])
def search(message):
    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        bot.reply_to(message, "❌ Используй: /s <запрос> <кол-во>")
        return

    query = args[1]
    try:
        limit = int(args[2])
    except:
        bot.reply_to(message, "❌ Кол-во должно быть числом")
        return

    params = {
        "q": f"{query} roblox script",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }

    r = requests.get(SEARCH_API, params=params, headers=HEADERS)

    if r.status_code != 200:
        bot.send_message(message.chat.id, f"❌ GitHub API error {r.status_code}")
        return

    repos = r.json().get("items", [])
    found = 0

    for repo in repos:
        if found >= limit:
            break

        owner = repo["owner"]["login"]
        name = repo["name"]

        contents_url = f"https://api.github.com/repos/{owner}/{name}/contents"
        c = requests.get(contents_url, headers=HEADERS)

        if c.status_code != 200:
            continue

        for f in c.json():
            if f["type"] == "file" and f["name"].endswith(".lua"):
                bot.send_message(
                    message.chat.id,
                    f"📦 {repo['full_name']}\n"
                    f"⭐ Stars: {repo['stargazers_count']}\n\n"
                    f"```lua\n"
                    f"loadstring(game:HttpGet(\"{f['download_url']}\"))()\n"
                    f"```",
                    parse_mode="Markdown"
                )
                found += 1
                break

    if found == 0:
        bot.send_message(message.chat.id, "❌ Lua скрипты не найдены")

print("Bot started")
bot.infinity_polling()
