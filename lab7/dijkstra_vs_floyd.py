import json
import time
import math
import heapq
import random


def load_graph_adj(filename: str):
    """Ваш JSON -> adjacency list: adj[u] = list[int], вершины 0..n-1."""
    with open(filename, "r") as f:
        g = json.load(f)

    n = len(g)
    adj = [[] for _ in range(n)]
    for u_str, neigh in g.items():
        u = int(u_str)
        adj[u] = [int(v) for v in neigh]
    return adj


# -------------------- 1) ДЕЙКСТРА: расстояния от 0 до всех --------------------
def dijkstra_distances_from_zero(adj):
    """
    Дейкстра (веса ребер = 1).
    Возвращает dist, parent и счетчики итераций.
    """
    n = len(adj)
    INF = float("inf")
    dist = [INF] * n
    parent = [-1] * n

    dist[0] = 0
    pq = [(0, 0)]  # (dist, node)

    # Фактические итерации/операции
    heap_pops = 0
    heap_pushes = 1
    relax_checks = 0
    relax_success = 0

    while pq:
        d, u = heapq.heappop(pq)
        heap_pops += 1
        if d != dist[u]:
            continue

        for v in adj[u]:
            relax_checks += 1
            nd = d + 1
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
                heap_pushes += 1
                relax_success += 1

    stats = {
        "heap_pops": heap_pops,
        "heap_pushes": heap_pushes,
        "relax_checks": relax_checks,
        "relax_success": relax_success,
    }
    return dist, parent, stats


# -------------------- 2) ОТЧЕТ: 2 пункта как ты попросил --------------------
def report_two_points(adj, floyd_max_n=800, sample_k=20, seed=42, print_path_limit=70):
    """
    Печатает отчет из 2 пунктов:
      1) расстояния от 0 до 20 случайных вершин (Дейкстра)
      2) сравнение Флойда и Дейкстры для пути 0 -> (n-1)
         (расстояние, путь, итерации, асимптотика)
    """
    n = len(adj)
    m = sum(len(adj[u]) for u in range(n)) // 2
    s, t = 0, n - 1

    def reconstruct_path_from_parent(parent, target):
        if target == 0:
            return [0]
        if parent[target] == -1:
            return []
        path = []
        cur = target
        while cur != -1:
            path.append(cur)
            if cur == 0:
                break
            cur = parent[cur]
        if path[-1] != 0:
            return []
        path.reverse()
        return path

    def format_path(path):
        if not path:
            return "(путь не найден)"
        if len(path) <= print_path_limit:
            return " -> ".join(map(str, path))
        head = " -> ".join(map(str, path[:print_path_limit // 2]))
        tail = " -> ".join(map(str, path[-print_path_limit // 2:]))
        return f"{head} -> ... -> {tail}  (вершин в пути: {len(path)})"

    line = "-" * 88

    # --- Запускаем Дейкстру 1 раз (она даст и пункт 1, и пункт 2) ---
    td0 = time.time()
    dist_d, parent_d, stats_d = dijkstra_distances_from_zero(adj)
    td1 = time.time()

    # ===================== ПУНКТ 1 =====================
    rng = random.Random(seed)
    candidates = list(range(1, n))  # исключим 0
    k = min(sample_k, len(candidates))
    sample_vertices = rng.sample(candidates, k) if k > 0 else []
    sample_vertices.sort()

    print(line)
    print("ОТЧЕТ (2 пункта)")
    print(line)
    print(f"Граф: n={n}, m={m}, средняя степень ~ {2*m/n:.2f}")
    print(line)

    print("1) Дейкстра: расстояния от вершины 0 до 20 случайных вершин")
    print(f"   (seed={seed}, выбрано вершин: {k})")
    print(f"   Время Дейкстры (0->все): {td1 - td0:.6f} сек")
    print("   Таблица: вершина -> расстояние")
    for v in sample_vertices:
        d = dist_d[v]
        d_out = int(d) if d != float("inf") else "inf"
        print(f"     {v:>6} -> {d_out}")
    print(line)

    # ===================== ПУНКТ 2 =====================
    print("2) Сравнение Флойда–Уоршелла и Дейкстры для пути 0 -> (n-1)")
    print(f"   Запрос: {s} -> {t}")
    print()

    # --- Dijkstra result for 0 -> last ---
    path_d = reconstruct_path_from_parent(parent_d, t)
    d_dist_last = dist_d[t]
    print("   [Дейкстра]")
    print(f"     Расстояние: {int(d_dist_last) if d_dist_last != float('inf') else 'inf'}")
    print(f"     Путь: {format_path(path_d)}")
    print("     Итерации/счетчики:")
    print(f"       relax_checks  = {stats_d['relax_checks']}")
    print(f"       relax_success = {stats_d['relax_success']}")
    print(f"       heap_pops     = {stats_d['heap_pops']}")
    print(f"       heap_pushes   = {stats_d['heap_pushes']}")
    print()

    # --- Floyd (if allowed) ---
    floyd_ran = (n <= floyd_max_n)
    fw_dist_last = None
    fw_path = []
    fw_iters = None
    fw_time = None

    if floyd_ran:
        INF = 10**9
        dist = [[INF] * n for _ in range(n)]
        nxt = [[-1] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0
            nxt[i][i] = i

        for u in range(n):
            for v in adj[u]:
                dist[u][v] = 1
                nxt[u][v] = v

        fw_iters = 0
        tf0 = time.time()
        for k_ in range(n):
            for i in range(n):
                dik = dist[i][k_]
                for j in range(n):
                    fw_iters += 1
                    nd = dik + dist[k_][j]
                    if nd < dist[i][j]:
                        dist[i][j] = nd
                        nxt[i][j] = nxt[i][k_]
        tf1 = time.time()
        fw_time = tf1 - tf0

        fw_dist_last = dist[s][t]
        # restore path 0->t using nxt
        if nxt[s][t] != -1:
            cur = s
            fw_path = [cur]
            while cur != t:
                cur = nxt[cur][t]
                if cur == -1:
                    fw_path = []
                    break
                fw_path.append(cur)

        print("   [Флойд–Уоршелл]")
        print(f"     Время: {fw_time:.6f} сек")
        print(f"     Расстояние: {fw_dist_last}")
        print(f"     Путь: {format_path(fw_path)}")
        print(f"     Итерации (k,i,j): {fw_iters}  (ожидаемо ~ n^3)")
        print(f"     Сверка расстояния с Дейкстрой: {'OK' if fw_dist_last == d_dist_last else 'НЕСОВПАДЕНИЕ'}")
        print()
    else:
        print("   [Флойд–Уоршелл]")
        print(f"     Пропущен: n={n} > floyd_max_n={floyd_max_n}")
        print("     Причина: память O(n^2) и время O(n^3) слишком дорогие для больших n.")
        print()

    # --- Asymptotics vs actual (численные оценки) ---
    logn = math.log2(n) if n > 1 else 1.0
    theo_fw = n**3
    theo_dijkstra_heap = (n + m) * logn
    theo_dijkstra_relax = 2 * m

    act_dijkstra_relax = stats_d["relax_checks"]
    act_dijkstra_heap_ops = stats_d["heap_pops"] + stats_d["heap_pushes"]

    print("   Сравнение фактических итераций с асимптотическими формулами")
    print("     Флойд:          Θ(n^3)")
    print("     Дейкстра(куча): Θ((n+m) log n) + просмотры ребер ~ Θ(m)")
    print()

    header = f"{'Метрика':<26} | {'Факт':>18} | {'Оценка':>18} | {'Факт/Оценка':>12}"
    print("   " + header)
    print("   " + "-" * len(header))

    def ratio(a, b):
        if a is None or b == 0:
            return "-"
        return f"{a / b:.6g}"

    print(f"   {'Dijkstra relax_checks':<26} | {act_dijkstra_relax:>18} | {theo_dijkstra_relax:>18.6g} | {ratio(act_dijkstra_relax, theo_dijkstra_relax):>12}")
    print(f"   {'Dijkstra heap_ops':<26} | {act_dijkstra_heap_ops:>18} | {theo_dijkstra_heap:>18.6g} | {ratio(act_dijkstra_heap_ops, theo_dijkstra_heap):>12}")

    if floyd_ran:
        print(f"   {'Floyd iterations':<26} | {fw_iters:>18} | {theo_fw:>18.6g} | {ratio(fw_iters, theo_fw):>12}")
    else:
        print(f"   {'Floyd iterations':<26} | {'(не считали)':>18} | {theo_fw:>18.6g} | {'-':>12}")

    print(line)

    return {
        "n": n,
        "m": m,
        "dijkstra": {
            "dist": dist_d,
            "path_0_to_last": path_d,
            "stats": stats_d,
            "time": td1 - td0,
        },
        "floyd": {
            "ran": floyd_ran,
            "dist_0_to_last": fw_dist_last,
            "path_0_to_last": fw_path,
            "iterations": fw_iters,
            "time": fw_time,
        }
    }


# Пример:
if __name__ == "__main__":
    adj = load_graph_adj("lab7/graph_n800.json")
    report_two_points(adj, floyd_max_n=800, sample_k=20, seed=42)