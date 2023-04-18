# -*- coding: utf-8 -*-

from typing import List
from math import log2, ceil
from random import randrange
import zlib
import Levenshtein
import statistics as st


def __hamming_common(src: List[List[int]], s_num: int, encode=True) -> int:
    s_range = range(s_num)
    errors = 0

    for i in src:
        sindrome = 0
        for s in s_range:
            sind = 0
            for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                for j in range(2 ** s):
                    if (p + j) > len(i):
                        break
                    sind ^= i[p + j - 1]

            if encode:
                i[2 ** s - 1] = sind
            else:
                sindrome += (2 ** s * sind)

        if (not encode) and sindrome:
            try:
                i[sindrome - 1] = int(not i[sindrome - 1])
            except IndexError:
                errors += 1

    return errors


def hamming_encode(msg: str, mode: int = 8) -> str:
    """
    Encoding the message with Hamming code.
    :param msg: Message string to encode
    :param mode: number of significant bits
    :return:
    """

    result = ""

    # msg_b = msg.encode("utf-8")
    msg_b = msg.encode("utf8")
    s_num = ceil(log2(log2(mode + 1) + mode + 1))   # number of control bits
    bit_seq = []
    for byte in msg_b:  # get bytes to binary values; every bits store to sublist
        bit_seq += list(map(int, f"{byte:08b}"))

    res_len = ceil((len(msg_b) * 8) / mode)     # length of result (bytes)
    bit_seq += [0] * (res_len * mode - len(bit_seq))    # filling zeros

    to_hamming = []

    for i in range(res_len):    # insert control bits into specified positions
        code = bit_seq[i * mode:i * mode + mode]
        for j in range(s_num):
            code.insert(2 ** j - 1, 0)
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, True)   # process

    for i in to_hamming:
        result += "".join(map(str, i))

    return result


def hamming_decode(msg: str, mode: int = 8):
    """
    Decoding the message with Hamming code.
    :param msg: Message string to decode
    :param mode: number of significant bits
    :return:
    """

    result = ""

    s_num = ceil(log2(log2(mode + 1) + mode + 1))   # number of control bits
    res_len = len(msg) // (mode + s_num)    # length of result (bytes)
    code_len = mode + s_num     # length of one code sequence

    to_hamming = []

    for i in range(res_len):    # convert binary-like string to int-list
        code = list(map(int, msg[i * code_len:i * code_len + code_len]))
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, False)  # process

    for i in to_hamming:    # delete control bits
        for j in range(s_num):
            i.pop(2 ** j - 1 - j)
        result += "".join(map(str, i))

    msg_l = []

    for i in range(len(result) // 8):   # convert from binary-sring value to integer
        val = "".join(result[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))

    # finally decode to a regular string
    try:
        result = bytes(msg_l).decode("utf-8")
    except UnicodeDecodeError:
        pass

    return result, errors


def noizer(msg: str, mode: int) -> str:
    """
    Generates an error in each element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(cnt):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize = randrange(code_len)
        to_noize[noize] = int(not to_noize[noize])
        result += "".join(map(str, to_noize))

    return result


def noizer4(msg: str, mode: int) -> str:
    """
    Generates up to 4 errors in each element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(cnt):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize1 = randrange(code_len)
        noize2 = randrange(code_len)
        noize3 = randrange(code_len)
        noize4 = randrange(code_len)
        to_noize[noize1] = int(not to_noize[noize1])
        to_noize[noize2] = int(not to_noize[noize2])
        to_noize[noize3] = int(not to_noize[noize3])
        to_noize[noize4] = int(not to_noize[noize4])
        result += "".join(map(str, to_noize))

    return result

def strComparison (str1, str2):
    sentences = str1.split(), str2.split()
    l = []
    for w1, w2 in zip(sentences[0], sentences[1]):
        l.append(Levenshtein.jaro_winkler(w1, w2))
    return st.mean(l)

if __name__ == '__main__':
    MODE = 43  # длина слова с контрольными битами составляет 49 => значащих битов в слове 43
    msg = 'Метод ветвей и границ (англ. branch and bound) — общий алгоритмический метод для нахождения оптимальных решений различных задач оптимизации, особенно дискретной и комбинаторной оптимизации. Метод является развитием метода полного перебора, в отличие от последнего — с отсевом подмножеств допустимых решений, заведомо не содержащих оптимальных решений.\n\nМетод ветвей и границ впервые предложен в 1960 году Алисой Лэнд и Элисон Дойг для решения задач целочисленного программирования.\n\nОбщая идея метода может быть описана на примере поиска минимума функции f(x) на множестве допустимых значений переменной x. Функция f и переменная x могут быть произвольной природы. Для метода ветвей и границ необходимы две процедуры: ветвление и нахождение оценок (границ).\n\nПроцедура ветвления состоит в разбиении множества допустимых значений переменной x на подобласти (подмножества) меньших размеров. Процедуру можно рекурсивно применять к подобластям. Полученные подобласти образуют дерево, называемое деревом поиска или деревом ветвей и границ. Узлами этого дерева являются построенные подобласти (подмножества множества значений переменной x).\n\nПроцедура нахождения оценок заключается в поиске верхних и нижних границ для решения задачи на подобласти допустимых значений переменной x.\n\nВ основе метода ветвей и границ лежит следующая идея: если нижняя граница значений функции на подобласти A дерева поиска больше, чем верхняя граница на какой-либо ранее просмотренной подобласти B, то A может быть исключена из дальнейшего рассмотрения (правило отсева). Обычно минимальную из полученных верхних оценок записывают в глобальную переменную m; любой узел дерева поиска, нижняя граница которого больше значения m, может быть исключён из дальнейшего рассмотрения.\n\nЕсли нижняя граница для узла дерева совпадает с верхней границей, то это значение является минимумом функции и достигается на соответствующей подобласти.\n\nМетод используется для решения некоторых NP-полных задач, в том числе задачи коммивояжёра и задачи о ранце.\n\nЗадача коммивояжёра (или TSP от англ. travelling salesman problem) — одна из самых известных задач комбинаторной оптимизации, заключающаяся в поиске самого выгодного маршрута, проходящего через указанные города хотя бы по одному разу с последующим возвратом в исходный город. В условиях задачи указываются критерий выгодности маршрута (кратчайший, самый дешёвый, совокупный критерий и тому подобное) и соответствующие матрицы расстояний, стоимости и тому подобного.'
    print(f'Сообщение:\n{msg}')
    checksum = zlib.crc32(msg.encode())
    print(f'Контрольная сумма: {checksum}')

    # Первая отправка (без ошибок)
    print('-----------ПЕРВАЯ ОТПРАВКА-----------')
    enc_msg = hamming_encode(msg, MODE)
    print(f'Кодированное сообщение:\n{enc_msg}')
    dec_msg, err = hamming_decode(enc_msg, MODE)
    dec_msg = dec_msg[:-2:]
    print(f'Раскодированное сообщение:\n{dec_msg}')
    print(
        f'Контрольная сумма: {zlib.crc32(dec_msg.encode())}, корректность: {zlib.crc32(dec_msg.encode()) == checksum}')
    print(f'MSG: {msg == dec_msg}')

    print(f'Совпадение строк: {strComparison(msg, dec_msg)}')

    # Вторая отправка (не более 1 ошибки на слово)
    print('-----------ВТОРАЯ ОТПРАВКА-----------')
    noize_msg = noizer(enc_msg, MODE)
    print(f'Кодированное сообщение с ошибками:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    dec_msg = dec_msg[:-2:]
    print(f'Раскодированное сообщение:\n{dec_msg}')
    print(
        f'Контрольная сумма: {zlib.crc32(dec_msg.encode())}, корректность: {zlib.crc32(dec_msg.encode()) == checksum}')
    print(f'MSG: {msg == dec_msg}')

    print(f'Совпадение строк: {strComparison(msg, dec_msg)}')

    # Третья отправка (4 ошибки на слово)
    print('-----------ТРЕТЬЯ ОТПРАВКА-----------')
    noize_msg = noizer4(enc_msg, MODE)
    print(f'Кодированное сообщение с ошибками:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    dec_msg = dec_msg[:-2:]
    print(f'Раскодированное сообщение:\n{dec_msg}')
    print(
        f'Контрольная сумма: {zlib.crc32(dec_msg.encode())}, корректность: {zlib.crc32(dec_msg.encode()) == checksum}, количество обнаруженных ошибок: {err}')

    print(f'Совпадение строк: {strComparison(msg, dec_msg)}')
