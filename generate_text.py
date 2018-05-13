import re
import argparse
import numpy as np
from collections import defaultdict
from fractions import Fraction


# Считывание данных из нашей модели. Возвращает отдельно слова и вероятности
def read_model_from_database():

    return model_words, model_probabilities


# Генерация текста и запись его в файл (в stdout)
def generate_text_for_chat(chat_id, length):
    # Считывание модели для данного чата
    model_words, model_probabilities = read_model_from_database()

    # Генерация и вывод слов
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

        # Вывод слова
        if is_space:
            result_file.write(' ')
        result_file.write(next_word)
