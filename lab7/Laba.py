import random
import json
from collections import deque


def generate_graph(n):
    if n < 15:
        raise ValueError("Число вершин должно быть не меньше 15.")

    graph = {i: set() for i in range(n)}
    edge_count = 0

    def add_edge(u, v):
        nonlocal edge_count
        if u == v or v in graph[u]:
            return False
        graph[u].add(v)
        graph[v].add(u)
        edge_count += 1
        return True

    print(f"--- Генерация графа для n = {n} ---")

    # Шаг 1 и 2: Встраиваем обязательные подграфы K_5 на вершинах 0..4
    for i in range(5):
        for j in range(i + 1, 5):
            add_edge(i, j)

    # K_5,5 на вершинах 5..14 (доли 5-9 и 10-14)
    k55_part1_nodes = range(5, 10)
    k55_part2_nodes = range(10, 15)
    for u in k55_part1_nodes:
        for v in k55_part2_nodes:
            add_edge(u, v)

    # Шаг 3: Обеспечение связности
    print("Обеспечиваем связность графа (улучшенный метод)...")
    add_edge(4, 5)  # Соединяем K_5 и K_5,5
    if n > 15:
        add_edge(14, 15)  # Присоединяем хвост
        for i in range(15, n - 1):
            add_edge(i, i + 1)
    print(f"Рёбер после обеспечения связности: {edge_count}")

    target_edges = int((n * n ** 0.5) / 2)
    print(f"Целевое количество рёбер: {target_edges}")

    # Множества для быстрой проверки принадлежности к долям
    k55_part1_set = set(k55_part1_nodes)
    k55_part2_set = set(k55_part2_nodes)

    while edge_count < target_edges:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)

        # ПРОВЕРКА: не является ли ребро "запрещенным" для K_5,5
        is_in_part1 = u in k55_part1_set and v in k55_part1_set
        is_in_part2 = u in k55_part2_set and v in k55_part2_set

        if is_in_part1 or is_in_part2:
            continue

        add_edge(u, v)

    print(f"Генерация для n={n} завершена. Рёбер: {edge_count}.")
    return graph


def verify_k5(graph, nodes = range(5)): # Полный ли подграф на данных вершинах (K_5)
    for i in nodes:
        for j in range(i + 1, nodes.stop):
            if j not in graph[i]:
                print(f"ОШИБКА K_5: Отсутствует ребро между {i} и {j}.")
                return False
    return True


def verify_k55(graph, part1 = range(5, 10), part2 = range(10, 15)): # Полный двудольный ли подграф на данных вершинах (K_55)
    # 1. Проверяем наличие всех рёбер между долями
    for u in part1:
        for v in part2:
            if v not in graph[u]:
                print(f"ОШИБКА K_5,5: Отсутствует ребро между долями ({u}, {v}).")
                return False

    # 2. Проверяем отсутствие рёбер внутри долей
    all_part1_nodes = set(part1)
    for u in part1:
        if not graph[u].isdisjoint(all_part1_nodes - {u}):
            print(f"ОШИБКА K_5,5: Найдено ребро внутри первой доли у вершины {u}.")
            return False

    all_part2_nodes = set(part2)
    for v in part2:
        if not graph[v].isdisjoint(all_part2_nodes - {v}):
            print(f"ОШИБКА K_5,5: Найдено ребро внутри второй доли у вершины {v}.")
            return False

    return True


def is_connected(graph): # Связный ли граф
    if not graph:
        return True

    start_node = next(iter(graph))  # Любая вершина для старта
    visited = {start_node}
    queue = deque([start_node])

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    if len(visited) != len(graph):
        print(f"ОШИБКА СВЯЗНОСТИ: Посещено {len(visited)} из {len(graph)} вершин.")
        return False
    return True


def verify_properties(graph):
    n = len(graph)
    print(f"\n--- Верификация свойств графа на n = {n} ---")

    is_k5_ok = verify_k5(graph)
    print(f"Проверка наличия K_5: {'УСПЕХ' if is_k5_ok else 'ПРОВАЛ'}")

    is_k55_ok = verify_k55(graph)
    print(f"Проверка наличия K_5,5: {'УСПЕХ' if is_k55_ok else 'ПРОВАЛ'}")

    is_conn_ok = is_connected(graph)
    print(f"Проверка связности: {'УСПЕХ' if is_conn_ok else 'ПРОВАЛ'}")

    target_avg_degree = n ** 0.5
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2
    actual_avg_degree = (2 * edge_count) / n

    print("Проверка разряженности:")
    print(f"  - Целевая средняя степень: ~{target_avg_degree:.2f}")
    print(f"  - Фактическая средняя степень: {actual_avg_degree:.2f}")

    print("Проверка простоты и неориентированности: Гарантировано алгоритмом генерации.")
    print("--- Верификация завершена ---")


def save_graph_to_json(graph, filename):
    # Конвертируем ключи в строки, а множества-значения в списки
    json_compatible_graph = {str(k): sorted(list(v)) for k, v in graph.items()}

    with open(filename, 'w') as f:
        json.dump(json_compatible_graph, f, indent=4)
    print(f"Граф сохранен в файл: {filename}")


if __name__ == "__main__":
    N_VALUES = [800, 2100, 6500, 18000, 37000]

    for n_val in N_VALUES:
        my_graph = generate_graph(n_val)

        verify_properties(my_graph)

        file_name = f"graph_n{n_val}.json"
        save_graph_to_json(my_graph, file_name)
        print("-" * 40)