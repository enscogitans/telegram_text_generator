import re
from collections import defaultdict
import model_database as db


# Наш алфавит и используемая кодировка
alphabet = re.compile(u'[ёЁа-яА-Я0-9]+[-]?[ёЁа-яА-Я0-9]+|[.,?!;:]+')
encode_type = 'utf-8'


# Обрабатывает строки, возвращая отдельные слова, согласованные
# с алфавитом, и, при необходимости, в нижнем регистре
def token_generator(text, is_lower=False):
    for token in alphabet.findall(text):
        yield token.lower() if is_lower else token


# По словам (токенам) возвращает биграммы
def bigram_generator(tokens):
    t0 = '&'
    for t1 in tokens:
        yield t0, t1
        if re.fullmatch(r'[?!.]+', t1):
            t0 = '&'
        else:
            t0 = t1


# Подсчёт количества слов и пар слов из биграмм соответственно
def count_words_and_pairs(bigrams):
    word_freq = defaultdict(lambda: 0)
    pair_freq = defaultdict(lambda: 0)

    last_symbol = '&'
    word_freq['&'] = 1
    for (t0, t1) in bigrams:
        if re.fullmatch(r'[?!.]+', t1):
            word_freq['&'] += 1
        word_freq[t1] += 1
        pair_freq[(t0, t1)] += 1
        last_symbol = t1

    if re.fullmatch(r'[?!.]+', last_symbol):
        pair_freq[('&', '&')] += 1
    else:
        pair_freq[(last_symbol, '&')] += 1
    return word_freq, pair_freq


# Инициализация изменений нашей модели. По ключу хранится лист слов,
# которые могут идти после него с указаним количества встречаний
def initialise_changes(word_freq, pair_freq):
    changes = defaultdict(list)
    for (t0, t1), freq in pair_freq.items():
        changes[t0].append((t1, freq))
    return changes


# Обновление базы данных. Сохранение в модель всех биграм из текста
def update_model(chat_id, text):
    # Инициализация генератора биграмм
    tokens = token_generator(text)
    bigrams = bigram_generator(tokens)

    # Подсчёт количества слов и пар слов соответственно
    word_freq, pair_freq = count_words_and_pairs(bigrams)

    # Инициализация изменений нашей модели
    changes = initialise_changes(word_freq, pair_freq)

    # Сохранение изменений в базу данных
    for token_0, changes_values in changes.items():
        for (token_1, add_to_num) in changes_values:
            success = db.try_increase_num(chat_id, token_0, token_1, add_to_num)
            if not success:
                db.try_add_record(chat_id, token_0, token_1, add_to_num)
