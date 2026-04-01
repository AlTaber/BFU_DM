import math
import heapq
from collections import Counter
import os

def huffman_bit_length(text):
    """Вспомогательная функция для расчета бит по Хаффману (для сравнения)"""
    freq = Counter(text)
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return len(text)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]: pair[1] = '0' + pair[1]
        for pair in hi[1:]: pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    huff_dict = {pair[0]: pair[1] for pair in heap[0][1:]}
    total_bits = sum(freq[char] * len(code) for char, code in huff_dict.items())
    return total_bits

def lzw_encode_and_count_bits(text):
    """Кодирование LZW согласно описанию в методичке"""
    # 1. Создаем начальный словарь из уникальных символов текста
    alphabet = sorted(list(set(text)))
    if len(alphabet) > 64:
        print("ВНИМАНИЕ: В тексте больше 64 уникальных символов! Задание 0 требует не более 64.")
        
    # Инициализация словаря ("гнезд")
    dictionary = {char: i for i, char in enumerate(alphabet)}
    dict_size = len(alphabet)
    
    # Переменные для алгоритма
    w = ""
    compressed_indices = []
    
    # Для точного подсчета бит: размер индекса растет при увеличении словаря
    # Изначально нам нужно бит для кодирования начального алфавита
    current_bit_length = math.ceil(math.log2(max(dict_size, 2))) 
    total_lzw_bits = 0

    # 2. Основной цикл алгоритма LZW
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc # Самый длинный префикс найден, идем дальше
        else:
            # Выводим число n в выходной поток
            compressed_indices.append(dictionary[w])
            total_lzw_bits += current_bit_length
            
            # Добавим в словарь новое гнездо t+c
            dictionary[wc] = dict_size
            dict_size += 1
            
            # Увеличиваем размерность бит, если словарь превысил текущую степень двойки
            if dict_size > (1 << current_bit_length):
                current_bit_length += 1
                
            w = c

    # Не забываем про последний символ/строку
    if w:
        compressed_indices.append(dictionary[w])
        total_lzw_bits += current_bit_length

    return compressed_indices, total_lzw_bits, dict_size

def main():
    
    filename = "Prepared_text.txt" 
    
    if not os.path.exists(filename):
        print(f"Пожалуйста, создайте файл '{filename}' и поместите туда ваш текст.")
        return

    # Чтение файла
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    if not text:
        print("Файл пуст!")
        return

    print(f"Длина текста: {len(text)} символов")
    print("-" * 50)

    # 1. Равномерное 6-битовое кодирование
    # По условию уникальных символов <= 64, значит на каждый символ нужно ровно 6 бит
    uniform_6bit_size = len(text) * 6
    
    # 2. Кодирование Хаффмана (из задания 2)
    huffman_size = huffman_bit_length(text)
    
    # 3. Кодирование LZW
    lzw_indices, lzw_size, final_dict_size = lzw_encode_and_count_bits(text)
    
    # Вывод результатов
    print("=== РЕЗУЛЬТАТЫ СРАВНЕНИЯ КОЛИЧЕСТВА БИТ ===")
    print(f"1. Равномерные коды (6 бит/символ): {uniform_6bit_size:,} бит")
    print(f"2. Коды Хаффмана (из Задания 2):    {huffman_size:,} бит")
    print(f"3. Алгоритм LZW:                    {lzw_size:,} бит")
    print("-" * 50)
    
    # Статистика по LZW
    print("=== Статистика LZW ===")
    print(f"Количество индексов на выходе: {len(lzw_indices)}")
    print(f"Размер итогового словаря (гнезд): {final_dict_size}")
    
    # Выводы
    print("-" * 50)
    print("ВЫВОД ДЛЯ ОТЧЕТА:")
    best = min(uniform_6bit_size, huffman_size, lzw_size)
    if best == lzw_size:
        print("Алгоритм LZW показал наилучшее сжатие на данном тексте.")
    elif best == huffman_size:
        print("Алгоритм Хаффмана показал наилучшее сжатие на данном тексте.")
    else:
        print("Равномерное кодирование оказалось самым компактным (маловероятно для осмысленного текста).")

if __name__ == "__main__":
    main()