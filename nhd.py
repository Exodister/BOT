import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Ссылка для скачивания файла
FILE_URL = "https://aitanapa.ru/download/расписание/?wpdmdl=970&refresh=673b71f9314dc1731949049"
FILE_PATH = "raspisanie.pdf"  # Путь, куда будем сохранять файл
token = '7531474756:AAH5acUGDzUn6AS3HpfNeFsh2Ol1mBSwDyM'


# Функция для скачивания файла
def download_file():
    response = requests.get(FILE_URL)
    if response.status_code == 200:
        with open(FILE_PATH, 'wb') as f:
            f.write(response.content)
        return True
    return False

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я могу отправить тебе расписание. Напиши /getfile, чтобы получить файл.')

# Команда /getfile
async def getfile(update: Update, context: CallbackContext) -> None:
    if not os.path.exists(FILE_PATH):  # Проверяем, существует ли файл
        if not download_file():  # Если нет, скачиваем файл
            await update.message.reply_text('Не удалось скачать файл, попробуйте позже.')
            return
    await update.message.reply_document(document=open(FILE_PATH, 'rb'))

def main():
    # Вставьте свой токен сюда
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getfile", getfile))

    application.run_polling()

if __name__ == '__main__':
    main()
