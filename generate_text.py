import re
import numpy as np
from fractions import Fraction
import model_database as db


# Считывание данных чата из нашей модели. Возвращает отдельно слова и вероятности
def read_model_from_chat(chat_id):
    # Считывание из БД
    model_words, model_nums = db.get_tokens_and_nums_for_chat(chat_id)

    # Рассчёт вероятностей
    model_probabilities = dict()
    for key, val in model_nums.items():
        nums_total_for_token = db.get_sum_of_nums_for_token_in_chat(key, chat_id)
        model_probabilities[key] = [Fraction(num, nums_total_for_token) for num in model_nums[key]]

    return model_words, model_probabilities


# Генерация текста для чата
def generate_text_for_chat(chat_id, length=None):
    # Если длина не указана, выбирается случайно
    if length is None:
        length = np.random.randint(10, 30)

    # Считывание модели для данного чата
    model_words, model_probabilities = read_model_from_chat(chat_id)

    # Генерация первого слова
    prev_word = np.random.choice(model_words['&'])
    result = prev_word

    # Генерация и вывод последующих слов
    for i in range(1, length):
        next_word = np.random.choice(model_words[prev_word],
                                     p=model_probabilities[prev_word])

        # Ставить ли пробел перед очередным словом?
        # "Сдвиг" текущего слова в предыдущее
        is_space = False
        if re.fullmatch(r'[?!.]+', next_word):
            # Если точка и тп, пробел не нужен
            prev_word = '&'
            is_space = False
        else:
            # Если не запятая и тп, пробел нужен
            if not re.fullmatch(r'[,;:]+', next_word):
                is_space = True
            prev_word = next_word

        # Добавление слова в результат
        if is_space:
            result += ' '
        result += next_word

    return result
