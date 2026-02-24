import telebot
import requests
import re
import random

TOKEN = "8700268110:AAGtHJ2_Kkyv-b9ZKUVmv8d-L4VLieMV90E"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ---------- ПРОВЕРКА KEY ----------
def check_key(lua_code: str) -> str:
    keywords = [
        "key system", "getkey", "get_key", "enter key",
        "verify key", "checkkey", "linkvertise",
        "lootlinks", "work.ink", "key ="
    ]
    code = lua_code.lower()
    for k in keywords:
        if k in code:
            return "KEY: ❌"
    return "KEY: ✅"

# ---------- ПОИСК RAW СКРИПТОВ ----------
def search_scripts(game: str, limit: int):
    query = f"{game} roblox lua loadstring"
    url = f"https://api.github.com/search/code?q={query}&per_page=20"

    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []

    items = r.json().get("items", [])
    random.shuffle(items)

    raw_links = []
    for item in items:
        if len(raw_links) >= limit:
            break

        html_url = item["html_url"]
        raw_url = html_url.replace(
            "https://github.com/",
            "https://raw.githubusercontent.com/"
        ).replace("/blob/", "/")

        raw_links.append(raw_url)

    return raw_links

# ---------- КОМАНДА /s ----------
@bot.message_handler(commands=["s"])
def search_handler(message):
    try:
        args = message.text.split()
        game = args[1]
        count = int(args[2])
    except:
        bot.reply_to(message, "Используй: `/s игра количество`")
        return

    bot.send_message(message.chat.id, "🔎 Ищу скрипты...")

    links = search_scripts(game, count)

    if not links:
        bot.send_message(message.chat.id, "❌ Скрипты не найдены")
        return

    for link in links:
        try:
            r = requests.get(link, timeout=10)
            lua_code = r.text

            key_status = check_key(lua_code)

            msg = (
                f"{key_status}\n\n"
                "```lua\n"
                f'loadstring(game:HttpGet("{link}"))()\n'
                "```"
            )

            bot.send_message(message.chat.id, msg)

        except:
            continue

# ---------- СТАРТ ----------
bot.infinity_polling()
