import argparse
import time
import telepot
from telepot.loop import MessageLoop
import model_database as db
import train_model
import generate_text


# Создание парсера
def create_parser():
    parser = argparse.ArgumentParser(
        description='''Это программа для запуска бота'''
    )
    parser.add_argument('-t', '--token', required=True,
                        help='Токен вашего бота'
                        )
    parser.add_argument('-p', '--proxy', default=None,
                        help='''Прокси для подключения к интернету'''
                        )
    return parser


# Создание бота по токену и подключение прокси при необходимости
def create_bot(token, proxy=None):
    if proxy is not None:
        telepot.api.set_proxy(proxy)
    return telepot.Bot(token)


# Функция обработки сообщений
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        line = msg['text']

        if line != '/generate':
            train_model.update_model(chat_id, line)
        else:
            answer = generate_text.generate_text_for_chat(chat_id)
            bot.sendMessage(chat_id, answer)


if __name__ == '__main__':
    parser = create_parser()    # Парсер аргументов
    args = parser.parse_args()  # Аргументы, пришедшие от парсера

    db.create_database()        # Создание базы, если не существует
    bot = create_bot(args.token, args.proxy)  # Наш бот

    # Запускаем бесконечный цикл обработки сообщений
    MessageLoop(bot, handle).run_as_thread()
    while True:
        time.sleep(10)
