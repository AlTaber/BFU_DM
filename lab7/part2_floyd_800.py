import json
import time
import matplotlib.pyplot as plt

def load_graph(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def floyd_warshall(graph_dict):
    nodes = list(graph_dict.keys())
    n = len(nodes)
    
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    dist = [[float('inf')] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0
        
    for u, neighbors in graph_dict.items():
        u_idx = node_to_idx[u]
        for v in neighbors:
            v_idx = node_to_idx[str(v)]
            dist[u_idx][v_idx] = 1
            dist[v_idx][u_idx] = 1 
            
    iterations = 0
    start_time = time.time()
    
    print(f"Начинаю расчет для {n} вершин...")
    
    for k in range(n):
        if k % 100 == 0 and k > 0:
            print(f"Обработано {k}/{n} вершин. Прошло: {time.time() - start_time:.2f} сек.")
        for i in range(n):
            for j in range(n):
                iterations += 1
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    end_time = time.time()
    print(f"Расчет завершен! Затрачено времени: {end_time - start_time:.2f} сек.")
    print(f"Количество итераций: {iterations}")
    
    return dist

if __name__ == "__main__":
    try:
        filename = 'graph_n800.json'
        graph = load_graph(filename)
        dist_matrix = floyd_warshall(graph)
        
        # Сохранение тепловой карты (картинки)
        print("Генерирую картинку с матрицей...")
        plt.figure(figsize=(10, 8))
        plt.imshow(dist_matrix, cmap='viridis', interpolation='nearest')
        plt.colorbar(label='Расстояние (в ребрах)')
        plt.title('Матрица кратчайших расстояний (800 вершин)')
        plt.savefig('matrix_heatmap_800.png')
        print("Успех! Картинка сохранена как matrix_heatmap_800.png")
        
        # Сохранение текстового фрагмента
        with open('matrix_slice_800.txt', 'w') as f:
            f.write("Фрагмент матрицы расстояний(первые 10x10 вершин):\n")
            for row in dist_matrix[:10]:
                f.write("\t".join(str(int(x)) if x != float('inf') else 'inf' for x in row[:10]) + "\n")
        print("Успех! Фрагмент с числами сохранен как matrix_slice_800.txt")
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")