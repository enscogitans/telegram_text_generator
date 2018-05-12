import argparse
import time
import telepot
from telepot.loop import MessageLoop


# Создание парсера
def create_parser():
    parser = argparse.ArgumentParser(
        description='''Это очень интересное описание бота...'''
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
    bot.sendMessage(msg['chat']['id'], msg['text'])


if __name__ == '__main__':
    parser = create_parser()    # Парсер аргументов
    args = parser.parse_args()  # Аргументы, пришедшие от парсера

    bot = create_bot(args.token, args.proxy)  # Наш бот

    # Запускаем бесконечный цикл обработки сообщений
    MessageLoop(bot, handle).run_as_thread()
    while True:
        time.sleep(10)
