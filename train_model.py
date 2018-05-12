import re
from fractions import Fraction
from collections import defaultdict


# Наш алфавит и используемая кодировка
alphabet = re.compile(u'[ёЁа-яА-Я0-9]+[-]?[ёЁа-яА-Я0-9]+|[.,?!;:]+')
encode_type = 'utf-8'


# Обрабатывает строки, возвращая отдельные слова, согласованные
# с алфавитом, и, при необходимости, в нижнем регистре
def token_generator(lines, is_lower):
    for line in lines:
        for token in alphabet.findall(line):
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


# Инициализация нашей модели. По ключу хранится лист слов,
# которые могут идти после него с указаним вероятности (в виде рац. дроби)
def initialise_model(word_freq, pair_freq):
    model = defaultdict(list)
    for (t0, t1), freq in pair_freq.items():
        model[t0].append((t1, Fraction(freq, word_freq[t0])))
    return model


# Сохранение модели в файл model.txt в указанной папке
def save_model(model, model_path):
    with open('{}\\model.txt'.format(model_path), 'w',
              encoding=encode_type) as model_file:
        for key, lst in model.items():
            model_file.write(key)
            for (word, freq) in lst:
                model_file.write(' {} {}'.format(word, freq))
            model_file.write('\n')


def update_model(lines):
    # Инициализация генератора биграмм
    tokens = token_generator(lines)
    bigrams = bigram_generator(tokens)

    # Подсчёт количества слов и пар слов соответственно
    word_freq, pair_freq = count_words_and_pairs(bigrams)

    # Инициализация и сохранение нашей модели
    model = initialise_model(word_freq, pair_freq)
    save_model(model, args.model)
