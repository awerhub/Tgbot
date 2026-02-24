import telebot
import requests

TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

GITHUB_API = "https://api.github.com/search/repositories"

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
        "q": query + " roblox script",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }

    r = requests.get(GITHUB_API, params=params)

    if r.status_code != 200:
        bot.reply_to(message, "❌ Ошибка GitHub API")
        return

    data = r.json().get("items", [])

    if not data:
        bot.reply_to(message, "❌ Ничего не найдено")
        return

    bot.send_message(message.chat.id, f"🔍 Поиск по запросу: {query}\n")

    for repo in data:
        text = (
            f"📦 {repo['full_name']}\n"
            f"⭐ Stars: {repo['stargazers_count']}\n"
            f"🔗 {repo['html_url']}\n"
        )
        bot.send_message(message.chat.id, text)

print("Bot started")
bot.infinity_polling()
