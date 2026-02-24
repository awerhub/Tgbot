import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Бот запущен и работает 24/7 ✅")

@bot.message_handler(func=lambda m: m.text.startswith("/s"))
def search(message):
    query = message.text.replace("/s", "").strip()

    if not query:
        bot.reply_to(message, "Напиши запрос после /s\nПример: /s evade 1")
        return

    # пока заглушка
    bot.reply_to(
        message,
        f"🔍 Поиск по запросу:\n`{query}`\n\n(логика поиска будет добавлена)",
        parse_mode="Markdown"
    )

bot.infinity_polling(skip_pending=True)
