import math
import collections
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Node:
    # Класс для представления узла в дереве Хаффмана
    def __init__(self, char, freq):
        self.char = char      # Символ (для листьев) или None (для внутренних узлов)
        self.freq = freq      # Частота встречаемости символа или суммы частот потомков
        self.left = None      # Ссылка на левого потомка
        self.right = None     # Ссылка на правого потомка
        self.id = id(self)    # Уникальный идентификатор узла (нужен для построения графа в NetworkX)

    def __lt__(self, other):
        # Переопределение оператора "меньше" для корректной работы сортировки в куче (min-heap).
        # Узлы с меньшей частотой будут иметь более высокий приоритет.
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    # Функция для построения дерева Хаффмана на основе словаря частот
    
    # Создаем список узлов из словаря и преобразуем его в очередь с приоритетами (min-heap)
    heap = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    
    # Пока в куче остается больше одного дерева, продолжаем объединение
    while len(heap) > 1:
        # Извлекаем два узла с наименьшими частотами
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Создаем новый родительский узел с суммарной частотой и без символа
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        # Помещаем новый узел обратно в кучу
        heapq.heappush(heap, merged)
        
    # Возвращаем корень построенного дерева (последний оставшийся элемент в куче)
    return heap[0] if heap else None

def generate_codes(node, current_code, codes):
    # Рекурсивная функция для обхода дерева и генерации бинарных кодов
    if node is None:
        return
        
    # Если достигли листового узла (есть символ), сохраняем накопленный код в словарь
    if node.char is not None:
        codes[node.char] = current_code
        return
        
    # Идем влево — добавляем "0" к коду, идем вправо — добавляем "1"
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

def calculate_shannon_entropy(probabilities):
    # Вычисление информационной энтропии по формуле Шеннона: H = -sum(p * log2(p))
    return -sum(p * math.log2(p) for p in probabilities.values() if p > 0)

def assign_pos(node, depth, pos_dict, current_x):
    # Рекурсивная функция для вычисления координат (x, y) каждого узла 
    # Это необходимо для красивой отрисовки дерева с помощью NetworkX и Matplotlib
    if node is None:
        return current_x
    
    # Сначала обходим левое поддерево
    current_x = assign_pos(node.left, depth + 1, pos_dict, current_x)
    
    # Записываем позицию текущего узла: x — текущая координата, y — отрицательная глубина (чтобы дерево росло вниз)
    pos_dict[node.id] = (current_x, -depth)
    current_x += 1
    
    # Затем обходим правое поддерево
    current_x = assign_pos(node.right, depth + 1, pos_dict, current_x)
    
    return current_x

def build_graph(node, G, labels):
    # Функция для рекурсивного добавления узлов и ребер в граф NetworkX
    if node is None:
        return
    
    # Формируем метку для узла: если это лист, показываем символ и частоту, если внутренний узел — только частоту
    label = f"'{node.char}'\n{node.freq}" if node.char else str(node.freq)
    labels[node.id] = label
    G.add_node(node.id)
    
    # Если есть левый потомок, добавляем ребро с весом "0" и рекурсивно обрабатываем его
    if node.left:
        G.add_edge(node.id, node.left.id, weight="0")
        build_graph(node.left, G, labels)
        
    # Если есть правый потомок, добавляем ребро с весом "1" и рекурсивно обрабатываем его
    if node.right:
        G.add_edge(node.id, node.right.id, weight="1")
        build_graph(node.right, G, labels)

def encode_text(text, codes):
    # Преобразует исходный текст в строку бинарных кодов (для посимвольного кодирования)
    return "".join(codes[char] for char in text)

def encode_bigrams(bigrams, codes):
    # Преобразует список биграмм в строку бинарных кодов
    return "".join(codes[bg] for bg in bigrams)

def analyze_and_plot():
    # Главная функция, выполняющая чтение, анализ, кодирование и построение графиков
    try:
        # Попытка открыть файл с подготовленным текстом
        with open("Prepared_text.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Файл Prepared_text.txt не найден. Пожалуйста, создай его в директории со скриптом.")
        return

    # --- АНАЛИЗ ОДИНОЧНЫХ СИМВОЛОВ ---
    n_chars = len(text)
    # Подсчет частоты каждого символа
    char_counts = collections.Counter(text)
    # Вычисление вероятности появления каждого символа
    char_probs = {ch: count / n_chars for ch, count in char_counts.items()}
    
    # --- АНАЛИЗ БИГРАММ (ПАР СИМВОЛОВ) ---
    # Разбиение текста на пары символов (с шагом 2)
    bigrams = [text[i:i+2] for i in range(0, n_chars - 1, 2)]
    # Если количество символов нечетное, добавляем последний символ как отдельный элемент
    if n_chars % 2 != 0:
        bigrams.append(text[-1])
        
    n_bigrams = len(bigrams)
    # Подсчет частоты каждой биграммы
    bigram_counts = collections.Counter(bigrams)
    # Вычисление вероятности появления каждой биграммы
    bigram_probs = {bg: count / n_bigrams for bg, count in bigram_counts.items()}

    # --- КОДИРОВАНИЕ ХАФФМАНА ДЛЯ СИМВОЛОВ ---
    char_tree = build_huffman_tree(char_counts)
    char_codes = {}
    generate_codes(char_tree, "", char_codes)
    
    # Кодирование текста и сохранение в файл
    encoded_text_chars = encode_text(text, char_codes)
    with open("encoded_chars_huffman.txt", "w", encoding="utf-8") as f:
        f.write(encoded_text_chars)
    
    # Вычисление объемов для символов
    huffman_char_bits = len(encoded_text_chars)       # Фактический объем по Хаффману
    uniform_char_bits = n_chars * 6                   # Объем при равномерном 6-битном кодировании
    shannon_char_entropy = calculate_shannon_entropy(char_probs) # Энтропия
    shannon_char_bits = n_chars * shannon_char_entropy           # Теоретический минимум

    # --- КОДИРОВАНИЕ ХАФФМАНА ДЛЯ БИГРАММ ---
    bg_tree = build_huffman_tree(bigram_counts)
    bg_codes = {}
    generate_codes(bg_tree, "", bg_codes)
    
    # Кодирование текста биграммами и сохранение в файл
    encoded_text_bg = encode_bigrams(bigrams, bg_codes)
    with open("encoded_bigrams_huffman.txt", "w", encoding="utf-8") as f:
        f.write(encoded_text_bg)
    
    # Вычисление объемов для биграмм
    huffman_bg_bits = len(encoded_text_bg)
    # Для равномерного кода биграмм вычисляем необходимое количество бит на одну уникальную биграмму
    uniform_bg_bits = n_bigrams * math.ceil(math.log2(len(bigram_counts)))
    shannon_bg_entropy = calculate_shannon_entropy(bigram_probs)
    shannon_bg_bits = n_bigrams * shannon_bg_entropy

    # --- ВЫВОД РЕЗУЛЬТАТОВ В КОНСОЛЬ ---
    print("=== РЕЗУЛЬТАТЫ ДЛЯ СИМВОЛОВ ===")
    print(f"Всего символов: {n_chars}")
    print(f"Объем (равномерный 6-битный код): {uniform_char_bits} бит")
    print(f"Объем (код Хаффмана, фактический): {huffman_char_bits} бит")
    print(f"Энтропия по Шеннону: {shannon_char_entropy:.4f} бит/символ")
    print(f"Теоретический минимум Шеннона: {shannon_char_bits:.0f} бит\n")
    print("Текст, закодированный посимвольно, сохранен в файл encoded_chars_huffman.txt\n")

    print("=== РЕЗУЛЬТАТЫ ДЛЯ БИГРАММ ===")
    print(f"Всего биграмм: {n_bigrams}")
    print(f"Объем (равномерный код, {math.ceil(math.log2(len(bigram_counts)))} бит/пару): {uniform_bg_bits} бит")
    print(f"Объем (код Хаффмана, фактический): {huffman_bg_bits} бит")
    print(f"Энтропия по Шеннону: {shannon_bg_entropy:.4f} бит/пару")
    print(f"Теоретический минимум Шеннона: {shannon_bg_bits:.0f} бит\n")
    print("Текст, закодированный биграммами, сохранен в файл encoded_bigrams_huffman.txt\n")

    # --- ПОСТРОЕНИЕ ДИАГРАММ СРАВНЕНИЯ ОБЪЕМОВ ---
    # Создаем фигуру с двумя графиками (1 строка, 2 столбца)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Данные для графика одиночных символов
    labels_char = ["Равномерный (6 бит)", "Хаффман", "Минимум Шеннона"]
    values_char = [uniform_char_bits, huffman_char_bits, shannon_char_bits]
    colors_char = ["#ff9999", "#66b3ff", "#99ff99"]
    
    # Отрисовка первого графика (символы)
    ax1.bar(labels_char, values_char, color=colors_char)
    ax1.set_title("Сравнение объемов данных (Одиночные символы)")
    ax1.set_ylabel("Количество бит")
    # Добавление числовых значений над столбцами
    for i, v in enumerate(values_char):
        ax1.text(i, v + 1000, f"{int(v)}", ha="center", fontweight="normal")

    # Данные для графика биграмм
    labels_bg = ["Равномерный", "Хаффман", "Минимум Шеннона"]
    values_bg = [uniform_bg_bits, huffman_bg_bits, shannon_bg_bits]
    
    # Отрисовка второго графика (биграммы)
    ax2.bar(labels_bg, values_bg, color=colors_char)
    ax2.set_title("Сравнение объемов данных (Биграммы)")
    ax2.set_ylabel("Количество бит")
    for i, v in enumerate(values_bg):
        ax2.text(i, v + 1000, f"{int(v)}", ha="center", fontweight="normal")

    # Сохранение графиков в файл
    plt.tight_layout()
    plt.savefig("comparison_plots.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Диаграмма сравнения объемов сохранена в файл comparison_plots.png")

    # --- ПОСТРОЕНИЕ ДЕРЕВА ХАФФМАНА ДЛЯ СИМВОЛОВ ---
    G = nx.DiGraph()
    labels = {}
    build_graph(char_tree, G, labels) # Заполнение графа узлами и ребрами
    
    pos = {}
    assign_pos(char_tree, 0, pos, 0)  # Расчет координат узлов для визуализации
    
    # Настройка размера изображения для дерева (оно может быть очень широким)
    plt.figure(figsize=(60, 25))
    
    # Отрисовка узлов графа
    nx.draw(G, pos, with_labels=False, node_size=1200, node_color="lightblue", edge_color="gray", arrows=False)
    # Отрисовка текста внутри узлов (символы и частоты)
    nx.draw_networkx_labels(G, pos, labels, font_size=11)
    
    # Получение весов ребер ("0" или "1") и их отрисовка
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    
    plt.title("Дерево кодирования Хаффмана (для одиночных символов)", fontsize=28)
    plt.axis("off") # Скрытие осей координат
    
    # Сохранение дерева в файл
    plt.savefig("huffman_tree.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Диаграмма дерева Хаффмана сохранена в файл huffman_tree.png")

if __name__ == "__main__":
    # Точка входа в программу. Код выполнится только если скрипт запущен напрямую, а не импортирован.
    analyze_and_plot()