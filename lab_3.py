#!/usr/bin/env python3
"""
Лабораторная работа №3: Методы кодирования
Вариант 7
"""

import heapq
from decimal import Decimal, getcontext
import math


def task1_hamming_code():
    """Код Хемминга"""
    print("=== ЗАДАНИЕ 1: КОД ХЕММИНГА ===\n")
    
    text = "Pentium "
    print(f"Исходная строка: '{text}'")
    
    # Переводим в двоичный код
    binary_str = ''
    for c in text:
        binary_str += format(ord(c), '08b')
    
    print(f"Двоичный ANSI код: {binary_str}")
    print(f"Длина: {len(binary_str)} бит")
    
    # Разбиваем на блоки
    block1 = binary_str[:32]
    block2 = binary_str[32:]
    print(f"\nБлок 1: {block1}")
    print(f"Блок 2: {block2}")
    
    def add_parity_bits(data):
        """Добавляем контрольные биты Хемминга"""
        n = len(data)
        r = 0
        while (1 << r) < n + r + 1:
            r += 1
        
        total = n + r
        code = [0] * (total + 1)  # 1-индексация
        
        # Расставляем биты данных
        j = 0
        for i in range(1, total + 1):
            if i & (i - 1) != 0:  # не степень двойки
                code[i] = int(data[j])
                j += 1
        
        # Считаем контрольные биты
        for i in range(r):
            pos = 1 << i
            parity = 0
            for k in range(1, total + 1):
                if k & pos:
                    parity ^= code[k]
            code[pos] = parity
        
        return code[1:]
    
    def find_error(code):
        """Находим позицию ошибки"""
        n = len(code)
        r = 0
        while (1 << r) <= n:
            r += 1
        
        error_pos = 0
        for i in range(r):
            pos = 1 << i
            parity = 0
            for k in range(1, n + 1):
                if k & pos:
                    parity ^= code[k - 1]
            if parity:
                error_pos += pos
        return error_pos
    
    def get_data(code):
        """Извлекаем данные без контрольных битов"""
        data = []
        for i in range(1, len(code) + 1):
            if i & (i - 1) != 0:
                data.append(code[i - 1])
        return data
    
    # Кодируем
    enc1 = add_parity_bits(block1)
    enc2 = add_parity_bits(block2)
    print(f"\nЗакодированный блок 1 ({len(enc1)} бит): {''.join(map(str, enc1))}")
    print(f"Закодированный блок 2 ({len(enc2)} бит): {''.join(map(str, enc2))}")
    
    # Вносим ошибки
    err1 = enc1.copy()
    err2 = enc2.copy()
    err1[4] ^= 1  # 5-й бит (индекс 4)
    err2[20] ^= 1  # 21-й бит (индекс 20)
    
    print(f"\nВнесена ошибка в бит 5 блока 1")
    print(f"Внесена ошибка в бит 21 блока 2")
    print(f"Блок 1 с ошибкой: {''.join(map(str, err1))}")
    print(f"Блок 2 с ошибкой: {''.join(map(str, err2))}")
    
    # Находим ошибки
    pos1 = find_error(err1)
    pos2 = find_error(err2)
    print(f"\nОбнаружена ошибка в блоке 1 на позиции: {pos1}")
    print(f"Обнаружена ошибка в блоке 2 на позиции: {pos2}")
    
    # Исправляем
    err1[pos1 - 1] ^= 1
    err2[pos2 - 1] ^= 1
    
    # Извлекаем данные
    data1 = get_data(err1)
    data2 = get_data(err2)
    result_binary = ''.join(map(str, data1 + data2))
    
    # Переводим обратно в текст
    result = ''
    for i in range(0, len(result_binary), 8):
        result += chr(int(result_binary[i:i+8], 2))
    
    print(f"\nВосстановленная строка: '{result}'")
    print(f"Проверка: {'OK' if result == text else 'ОШИБКА'}")


def task2_hamming_distance():
    """Расстояние Хемминга"""
    print("=== ЗАДАНИЕ 2: РАССТОЯНИЕ ХЕММИНГА ===\n")
    
    letters = "иклмнопр"
    print(f"Буквы: {letters}")
    
    def hamming_dist(a, b):
        return sum(x != y for x, y in zip(a, b))
    
    # Часть 1: расстояние >= 2
    print("\n--- Коды с расстоянием >= 2 ---")
    print("Используем 4 бита данных + 1 бит четности")
    
    codes_d2 = []
    for i in range(8):
        base = format(i, '04b')
        parity = str(base.count('1') % 2)
        codes_d2.append(base + parity)
    
    for letter, code in zip(letters, codes_d2):
        print(f"  {letter}: {code}")
    
    # Проверяем минимальное расстояние
    min_d = 100
    for i in range(len(codes_d2)):
        for j in range(i + 1, len(codes_d2)):
            d = hamming_dist(codes_d2[i], codes_d2[j])
            if d < min_d:
                min_d = d
    print(f"Минимальное расстояние: {min_d}")
    
    # Демонстрация обнаружения
    print("\nДемонстрация обнаружения ошибки:")
    original = codes_d2[0]
    print(f"Исходный код 'и': {original}")
    corrupted = original[:2] + ('1' if original[2] == '0' else '0') + original[3:]
    print(f"С ошибкой в бите 3: {corrupted}")
    ones = corrupted.count('1')
    print(f"Единиц: {ones} - {'нечетно, ОШИБКА!' if ones % 2 != 0 else 'четно, ок'}")
    
    # Часть 2: расстояние >= 3
    print("\n--- Коды с расстоянием >= 3 ---")
    
    codes_d3 = [
        "0000000",
        "0001111",
        "0110011",
        "0111100",
        "1010101",
        "1011010",
        "1100110",
        "1101001",
    ]
    
    for letter, code in zip(letters, codes_d3):
        print(f"  {letter}: {code}")
    
    # Проверяем расстояние
    min_d = 100
    for i in range(len(codes_d3)):
        for j in range(i + 1, len(codes_d3)):
            d = hamming_dist(codes_d3[i], codes_d3[j])
            if d < min_d:
                min_d = d
    print(f"Минимальное расстояние: {min_d}")
    
    # Демонстрация исправления
    print("\nДемонстрация исправления ошибки:")
    original = codes_d3[1]  # 'к'
    print(f"Исходный код 'к': {original}")
    corrupted = original[:3] + ('1' if original[3] == '0' else '0') + original[4:]
    print(f"С ошибкой в бите 4: {corrupted}")
    
    # Ищем ближайший
    min_dist = 100
    closest = -1
    for i, code in enumerate(codes_d3):
        d = hamming_dist(corrupted, code)
        if d < min_dist:
            min_dist = d
            closest = i
    print(f"Ближайший код: {codes_d3[closest]} = '{letters[closest]}'")


def task3_rle():
    """RLE сжатие"""
    print("=== ЗАДАНИЕ 3: RLE СЖАТИЕ ===\n")
    
    text = "aaaaaaaaaaaaadghtttttttttttyiklooooooop"
    print(f"Исходная строка: {text}")
    print(f"Длина: {len(text)} байт")
    
    def rle_encode(data):
        result = []
        i = 0
        while i < len(data):
            # Считаем повторы
            count = 1
            while i + count < len(data) and data[i + count] == data[i]:
                count += 1
            
            if count >= 2:
                # Повторяющийся символ
                result.append(count)
                result.append(ord(data[i]))
                i += count
            else:
                # Собираем неповторяющиеся
                non_rep = []
                while i < len(data):
                    if i + 1 < len(data) and data[i] == data[i + 1]:
                        break
                    non_rep.append(data[i])
                    i += 1
                
                if non_rep:
                    result.append(0)
                    result.append(len(non_rep))
                    for c in non_rep:
                        result.append(ord(c))
        
        return result
    
    def rle_decode(encoded):
        result = ''
        i = 0
        while i < len(encoded):
            if encoded[i] > 0:
                count = encoded[i]
                char = chr(encoded[i + 1])
                result += char * count
                i += 2
            else:
                count = encoded[i + 1]
                for j in range(count):
                    result += chr(encoded[i + 2 + j])
                i += 2 + count
        return result
    
    encoded = rle_encode(text)
    print(f"\nЗакодировано: {encoded}")
    print(f"Размер: {len(encoded)} байт")
    
    # Расшифровка кода
    print("\nРасшифровка:")
    i = 0
    while i < len(encoded):
        if encoded[i] > 0:
            print(f"  {encoded[i]}, {encoded[i+1]} -> '{chr(encoded[i+1])}' x {encoded[i]}")
            i += 2
        else:
            count = encoded[i + 1]
            chars = ''.join(chr(c) for c in encoded[i+2:i+2+count])
            print(f"  0, {count}, ... -> неповторяющиеся: '{chars}'")
            i += 2 + count
    
    # Проверка
    decoded = rle_decode(encoded)
    print(f"\nДекодировано: {decoded}")
    print(f"Проверка: {'OK' if decoded == text else 'ОШИБКА'}")
    
    # Статистика
    original = len(text)
    compressed = len(encoded)
    print(f"\nСтатистика:")
    print(f"  Исходный размер: {original} байт")
    print(f"  Сжатый размер: {compressed} байт")
    print(f"  Коэффициент сжатия: {original / compressed:.2f}")
    print(f"  Степень сжатия: {(1 - compressed / original) * 100:.1f}%")


def task4_huffman():
    """Алгоритм Хаффмана"""
    print("=== ЗАДАНИЕ 4: АЛГОРИТМ ХАФФМАНА ===\n")
    
    freq = {'A': 1, 'B': 2, 'C': 9, 'D': 9, 'E': 19, 'F': 27, 'G': 33}
    total = sum(freq.values())
    
    print("Частоты символов:")
    for c, f in freq.items():
        print(f"  {c}: {f}")
    
    # Узел дерева
    class Node:
        def __init__(self, char, f):
            self.char = char
            self.freq = f
            self.left = None
            self.right = None
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    # Строим дерево
    heap = [Node(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    
    print("\nПостроение дерева:")
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        l_name = left.char if left.char else f"({left.freq})"
        r_name = right.char if right.char else f"({right.freq})"
        print(f"  Объединяем {l_name} и {r_name} -> ({merged.freq})")
        
        heapq.heappush(heap, merged)
    
    root = heap[0]
    
    # Получаем коды
    codes = {}
    
    def build_codes(node, code=''):
        if node.char:
            codes[node.char] = code if code else '0'
        else:
            build_codes(node.left, code + '0')
            build_codes(node.right, code + '1')
    
    build_codes(root)
    
    print("\nКоды символов:")
    total_bits = 0
    for c in sorted(codes.keys()):
        bits = len(codes[c]) * freq[c]
        total_bits += bits
        print(f"  {c}: {codes[c]} (длина {len(codes[c])})")
    
    # Примеры
    print("\nПримеры кодирования:")
    for word in ["CAFE", "BAD", "EDGE"]:
        encoded = ''.join(codes[c] for c in word)
        print(f"  {word} -> {encoded}")
    
    # Декодирование
    print("\nПример декодирования:")
    test = "110010011110"
    print(f"  Код: {test}")
    
    result = ''
    node = root
    for bit in test:
        node = node.left if bit == '0' else node.right
        if node.char:
            result += node.char
            node = root
    print(f"  Результат: {result}")
    
    # Статистика
    uniform = total * 3  # 3 бита на символ достаточно для 7 символов
    print(f"\nСтатистика:")
    print(f"  Равномерный код (3 бит/символ): {uniform} бит")
    print(f"  Код Хаффмана: {total_bits} бит")
    print(f"  Коэффициент сжатия: {uniform / total_bits:.2f}")
    print(f"  Степень сжатия: {(1 - total_bits / uniform) * 100:.1f}%")


def task5_arithmetic():
    """Арифметическое кодирование"""
    print("=== ЗАДАНИЕ 5: АРИФМЕТИЧЕСКОЕ КОДИРОВАНИЕ ===\n")
    
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f']
    probs = [0.10, 0.10, 0.05, 0.55, 0.10, 0.10]
    
    print("Алфавит и вероятности:")
    for c, p in zip(alphabet, probs):
        print(f"  {c}: {p}")
    
    # Кумулятивные вероятности
    cumul = [0.0]
    for p in probs:
        cumul.append(cumul[-1] + p)
    
    print("\nИнтервалы:")
    for i, c in enumerate(alphabet):
        print(f"  {c}: [{cumul[i]:.2f}, {cumul[i+1]:.2f})")
    
    text = "aecdfb"
    print(f"\nКодируем: '{text}'")
    
    # Используем Decimal для точности
    getcontext().prec = 50
    cumul_d = [Decimal(str(c)) for c in cumul]
    
    low = Decimal('0')
    high = Decimal('1')
    
    print("\nПроцесс кодирования:")
    for char in text:
        idx = alphabet.index(char)
        width = high - low
        high = low + width * cumul_d[idx + 1]
        low = low + width * cumul_d[idx]
        print(f"  {char}: [{float(low):.10f}, {float(high):.10f})")
    
    print(f"\nИтоговый интервал: [{float(low):.15f}, {float(high):.15f})")
    
    # Переводим в двоичный код
    binary = ''
    lo, hi = Decimal('0'), Decimal('1')
    
    for _ in range(64):
        mid = (lo + hi) / 2
        if mid <= low:
            binary += '1'
            lo = mid
        else:
            binary += '0'
            hi = mid
        
        if lo >= low and hi <= high:
            break
    
    print(f"\nДвоичный код: {binary}")
    print(f"Длина: {len(binary)} бит")
    
    # Проверка значения
    value = Decimal('0')
    for i, b in enumerate(binary):
        if b == '1':
            value += Decimal('2') ** (-(i + 1))
    print(f"Значение: {float(value):.15f}")
    print(f"Попадает в интервал: {'OK' if low <= value < high else 'ОШИБКА'}")
    
    # Статистика
    uniform = len(text) * 3  # 3 бита для 6 символов
    arith = len(binary)
    print(f"\nСтатистика:")
    print(f"  Равномерный код (3 бит/символ): {uniform} бит")
    print(f"  Арифметический код: {arith} бит")
    print(f"  Коэффициент сжатия: {uniform / arith:.2f}")
    print(f"  Степень сжатия: {(1 - arith / uniform) * 100:.1f}%")


if __name__ == "__main__":
    print("Лабораторная работа №3: Методы кодирования")
    print("Вариант 7\n")
    
    while True:
        print("\n1 - Код Хемминга")
        print("2 - Расстояние Хемминга")
        print("3 - RLE сжатие")
        print("4 - Алгоритм Хаффмана")
        print("5 - Арифметическое кодирование")
        
        choice = input("> ").strip().lower()
        print()
        
        if choice == '1':
            task1_hamming_code()
        elif choice == '2':
            task2_hamming_distance()
        elif choice == '3':
            task3_rle()
        elif choice == '4':
            task4_huffman()
        elif choice == '5':
            task5_arithmetic()