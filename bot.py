import asyncio
import random
import os
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

RHYMES_MIKA = [
    "Мика-Мика, где улыбка? Съела кошка всю копилку! 😄",
    "Мика-Мика, ты — загадка, жизнь у Мики — шоколадка! 🍫",
    "Мика-Мика, как гвоздика, ярче солнца в небе Мика! ☀️",
    "Мика-Мика, крикнул зайка: поиграй со мной давай-ка! 🐰",
    "Мика-Мика, где косичка? Съела кошка — вот и птичка! 🐱",
    "Мика-Мика — звук как скрипка, на лице большая улыбка! 🎻",
    "Мика-Мика спит в кроватке, снятся Мике шоколадки! 🛏️",
    "Мика-Мика пьёт кефирку, потеряла всю копирку! 📄",
    "Мика-Мика ела блинчик, нашла в блинчике пингвинчик! 🐧",
    "Мика-Мика, крикнул ослик: ты красивей всех на свете! 🫏",
]

RHYMES_MIKAEL = [
    "Микаэл — орёл-орёл, по делам туда-сюда пошёл! 🦅",
    "Микаэл сварил омлет, ел два часа — вот дан ответ! 🍳",
    "Микаэл, Микаэл — кто котлеты в суп задел? 🍖",
    "Микаэл пошёл гулять, взял зонтик, чтоб не намокать! ☂️",
    "Микаэл — большой герой, победил вчера... покой! 😴",
    "Микаэл читает книжку, вместо книжки съел коврижку! 📚",
    "Микаэл купил кроссовки, потерял их с двух попытки! 👟",
    "Микаэл сказал: «привет!» — эхо крикнуло в ответ! 🏔️",
    "Микаэл, Микаэл — целый торт один он съел! 🎂",
    "Микаэл пошёл на пляж, взял с собою чемодаж! 🏖️",
]

ALL_RHYMES = RHYMES_MIKA + RHYMES_MIKAEL


async def send_rhyme(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    rhyme = random.choice(ALL_RHYMES)
    await context.bot.send_message(chat_id=chat_id, text=rhyme)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Remove existing jobs for this chat
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.run_repeating(
        send_rhyme,
        interval=15 * 60,
        first=5,
        name=str(chat_id),
        data=chat_id,
    )

    await update.message.reply_text(
        "🎉 Бот запущен! Каждые 15 минут буду присылать смешные рифмы про Мику и Микаэла!\n\n"
        "Команды:\n"
        "/start — запустить бота\n"
        "/stop — остановить\n"
        "/rhyme — получить рифму прямо сейчас"
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
        await update.message.reply_text("⛔ Рифмы остановлены. Скучновато без них!")
    else:
        await update.message.reply_text("Бот и так не запущен. Нажми /start!")


async def rhyme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ALL_RHYMES))


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Нужен TELEGRAM_BOT_TOKEN в переменных окружения")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("rhyme", rhyme))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
