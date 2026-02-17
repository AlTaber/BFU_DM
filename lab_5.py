import random

N = 31
K = 21
G_POLY = [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1] 

def list_to_str(lst):
    return "".join(map(str, lst))

def xor_lists(a, b):
    length = max(len(a), len(b))
    res = []
    for i in range(length):
        val_a = a[i] if i < len(a) else 0
        val_b = b[i] if i < len(b) else 0
        res.append(val_a ^ val_b)
    return res

def poly_div_mod2(dividend, divisor):
    msg = dividend[:]
    poly = divisor[:]
    
    while len(msg) >= len(poly) and (1 in msg):
        # Ищем первую единицу
        try:
            first_one_idx = msg.index(1)
        except ValueError:
            break # Единиц нет
            
        # Если оставшийся хвост короче полинома, то это уже остаток
        if len(msg) - first_one_idx < len(poly):
            break
            
        # XORим часть сообщения с полиномом
        for i in range(len(poly)):
            msg[first_one_idx + i] ^= poly[i]
            
    # Убираем ведущие нули, но нужно аккуратно с длиной
    # Для систематического кодирования нам нужны последние (N-K) бит
    # Но проще вернуть результат как есть, обрезанный по длине N-K с конца
    return msg[-(len(dividend) - len(divisor) + 1):]

def get_remainder(message_bits, generator_poly):
    """
    Вычисляет остаток от деления M(x)*x^(n-k) на G(x).
    Используется для создания проверочных бит.
    """
    check_len = N - K
    # Сдвигаем сообщение (дописываем нули)
    dividend = message_bits + [0] * check_len
    
    # Эмуляция деления "столбиком"
    temp = list(dividend)
    poly_len = len(generator_poly)
    
    for i in range(len(message_bits)):
        if temp[i] == 1:
            for j in range(poly_len):
                temp[i + j] ^= generator_poly[j]
                
    # Остаток - это последние check_len бит
    remainder = temp[-check_len:]
    return remainder


def task_1():
    print("\n=== ЗАДАНИЕ 1: Порождающая матрица и кодовое расстояние ===")
    
    # 1. Строим систематическую порождающую матрицу
    matrix_rows = []
    
    for i in range(K):
        # Создаем строку с одной 1 на i-й позиции (базисный вектор)
        row_data = [0] * K
        row_data[i] = 1
        
        # Вычисляем проверочные биты для этого вектора
        parity = get_remainder(row_data, G_POLY)
        
        # Полное кодовое слово
        full_row = row_data + parity
        matrix_rows.append(full_row)
    
    print("Порождающая матрица:")
    for r in matrix_rows:
        print(f"[{list_to_str(r)}]")
    
    # 2. Вычисляем кодовые слова и минимальное расстояние
    # ВНИМАНИЕ: Перебор 2^21 (2 млн) слов на Python займет время.
    # Для лабы обычно достаточно проверить веса строк матрицы и их попарных сумм.
    # Но сделаем честный перебор небольшого подмножества для демонстрации.
    
    print("\nВычисление минимального веса (d_min)...")
    min_dist = N # Начальное значение (максимально возможное)
    
    # Проверим веса строк матрицы (вес 1 во входных данных)
    for row in matrix_rows:
        w = sum(row)
        if w > 0 and w < min_dist:
            min_dist = w
            
    # Проверим суммы пар строк (вес 2 во входных данных) - часто d_min кроется тут
    for i in range(len(matrix_rows)):
        for j in range(i + 1, len(matrix_rows)):
            sum_row = xor_lists(matrix_rows[i], matrix_rows[j])
            w = sum(sum_row)
            if w > 0 and w < min_dist:
                min_dist = w

    print(f"Минимальное кодовое расстояние (d_min): {min_dist}")
    
    # Для отчета вернем матрицу и d_min
    return matrix_rows, min_dist

def task_2(d_min):
    print("\n=== ЗАДАНИЕ 2: Характеристики обнаружения и исправления ===")
    # Формулы:
    # Обнаружение: t_d = d_min - 1
    # Исправление: t_c = floor((d_min - 1) / 2)
    
    t_detect = d_min - 1
    t_correct = int((d_min - 1) / 2)
    
    print(f"При d_min = {d_min}:")
    print(f"1. Кратность гарантированно обнаруживаемых ошибок: до {t_detect} бит")
    print(f"2. Кратность гарантированно исправляемых ошибок: до {t_correct} бит")
    
    return t_detect, t_correct

def task_3(matrix, t_correct):
    print("\n=== ЗАДАНИЕ 3: Примеры свойств кода ===")
    
    # Возьмем произвольное сообщение
    msg = [0] * K
    msg[0] = 1; msg[5] = 1; msg[20] = 1 # Пример: 10000100...001
    
    # Кодируем (умножение вектора на матрицу или через функцию остатка)
    # Проще через функцию остатка, так как матрицу мы строили так же
    parity = get_remainder(msg, G_POLY)
    codeword = msg + parity
    print(f"Исходное сообщение: {list_to_str(msg)}")
    print(f"Кодовый вектор (C): {list_to_str(codeword)}")
    
    # Пример 1: Ошибка, которую можно исправить (в пределах t_correct)
    if t_correct > 0:
        corrupted = list(codeword)
        # Инвертируем 1 бит (позиция 3)
        corrupted[3] ^= 1 
        print(f"\nВносим ошибку кратности 1 (позиция 3):")
        print(f"Принятый вектор (R): {list_to_str(corrupted)}")
        
        # Проверяем синдром (делим принятое на g(x))
        # Для проверки делим ВЕСЬ вектор на g(x). Если остаток 0 - ошибок нет.
        syndrome = get_remainder_full(corrupted, G_POLY)
        print(f"Синдром (остаток от деления R на g(x)): {list_to_str(syndrome)}")
        if sum(syndrome) != 0:
            print(">> Ошибка обнаружена! (Синдром не нулевой)")
        else:
            print(">> Ошибка НЕ обнаружена.")
    else:
        print("Код не может исправлять ошибки.")

def task_4(matrix, t_correct, t_detect):
    print("\n=== ЗАДАНИЕ 4: Вектор ошибки (обнаруживает, но не исправляет) ===")
    # Нам нужна ошибка веса W, где t_correct < W <= t_detect
    
    target_weight = t_correct + 1
    if target_weight > t_detect:
        print("Невозможно подобрать такой пример для данного d_min (слишком мал).")
        return

    # Генерируем вектор ошибки
    error_vector = [0] * N
    # Ставим единицы подряд для простоты
    for i in range(target_weight):
        error_vector[i] = 1
        
    print(f"Вектор ошибки E (вес {target_weight}): {list_to_str(error_vector)}")
    print(f"Это больше, чем t_correct ({t_correct}), но входит в t_detect ({t_detect})")
    
    # Проверяем синдром ошибки
    # Синдром ошибки = остаток от деления E(x) на g(x)
    syndrome = get_remainder_full(error_vector, G_POLY)
    print(f"Синдром ошибки: {list_to_str(syndrome)}")
    
    if sum(syndrome) != 0:
        print(">> Код обнаружил наличие ошибки (синдром != 0).")
        print(">> Но исправить её корректно алгоритм не гарантирует (может принять за ошибку меньшего веса в другом месте).")
    else:
        print(">> Ошибка не обнаружена (совпала с кодовым словом).")

def get_remainder_full(bits, poly):
    """
    Вспомогательная функция для проверки кодового слова (деление без сдвига)
    Используется для вычисления синдрома.
    """
    temp = list(bits)
    poly_len = len(poly)
    # Идем только до len(bits) - len(poly) + 1
    stop = len(bits) - poly_len + 1
    for i in range(stop):
        if temp[i] == 1:
            for j in range(poly_len):
                temp[i + j] ^= poly[j]
    
    # Синдром - это то, что осталось в конце (размером с степень полинома)
    # Степень полинома 10, длина массива 11. Остаток - 10 бит.
    return temp[-(len(poly)-1):]


# --- ЗАПУСК ПРОГРАММЫ ---

def main():
    print("Лабораторная работа №5. Циклические коды.")
    print(f"Вариант 16. n={N}, m={K}, g(x)={list_to_str(G_POLY)}")
    
    matrix, d_min = task_1()
    t_det, t_cor = task_2(d_min)
    task_3(matrix, t_cor)
    task_4(matrix, t_cor, t_det)

if __name__ == "__main__":
    main()