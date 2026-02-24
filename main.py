import telebot
import requests

TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

SEARCH_API = "https://api.github.com/search/repositories"

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
        "per_page": limit
    }

    r = requests.get(SEARCH_API, params=params)
    if r.status_code != 200:
        bot.reply_to(message, "❌ Ошибка GitHub API")
        return

    repos = r.json().get("items", [])
    if not repos:
        bot.reply_to(message, "❌ Ничего не найдено")
        return

    sent = 0

    for repo in repos:
        if sent >= limit:
            break

        owner = repo["owner"]["login"]
        name = repo["name"]

        contents_url = f"https://api.github.com/repos/{owner}/{name}/contents"
        contents = requests.get(contents_url)

        if contents.status_code != 200:
            continue

        for file in contents.json():
            if file["type"] == "file" and file["name"].endswith(".lua"):
                msg = (
                    f"📦 {repo['full_name']}\n"
                    f"⭐ Stars: {repo['stargazers_count']}\n"
                    f"📄 {file['name']}\n\n"
                    f"```lua\n"
                    f"loadstring(game:HttpGet(\"{file['download_url']}\"))()\n"
                    f"```"
                )
                bot.send_message(message.chat.id, msg, parse_mode="Markdown")
                sent += 1
                break  # берём 1 lua с репо

    if sent == 0:
        bot.send_message(message.chat.id, "❌ Lua-скрипты не найдены")

print("Bot started")
bot.infinity_polling()
