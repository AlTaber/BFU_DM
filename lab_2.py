from collections import Counter
from functools import lru_cache
import sys

sys.setrecursionlimit(5000)

def task_1():
    source_word = "ЧЕРЕСПОЛОСИЦА"
    target_length = 5
    
    letter_counts = Counter(source_word) # {'Ч': 1, 'Е': 2, 'Р': 1, 'С': 2, 'П': 1, 'О': 3, 'Л': 1, 'И': 1, 'Ц': 1, 'А': 1}
    
    found_words_count = 0

    def backtrack(current_length):
        nonlocal found_words_count

        if current_length == target_length:
            found_words_count += 1
            return

        for char in letter_counts:
            if letter_counts[char] > 0:
                letter_counts[char] -= 1
                
                backtrack(current_length + 1)
                
                letter_counts[char] += 1

    backtrack(0)
    print(f"Задание 1: Количество различных слов = {found_words_count}")

def task_5():
    WIDTH = 19
    HEIGHT = 18
    
    @lru_cache(None)
    def count_paths_simple(x, y):
        if x == 0 and y == 0:
            return 1

        if x < 0 or y < 0:
            return 0
        
        return count_paths_simple(x - 1, y) + count_paths_simple(x, y - 1)

    result_part1 = count_paths_simple(WIDTH, HEIGHT)
    
    @lru_cache(None)
    def find_paths_forward(x, y, last_was_vertical):
        if x == WIDTH and y == HEIGHT:
            return 1
        if x > WIDTH or y > HEIGHT:
            return 0
        
        paths = 0
        
        paths += find_paths_forward(x + 1, y, False)
        
        if not last_was_vertical:
            paths += find_paths_forward(x, y + 1, True)
            
        return paths

    result_part2 = find_paths_forward(0, 0, False)

    print(f"Задание 5 (Всего путей): {result_part1}")
    print(f"Задание 5 (Без двух вертикальных подряд): {result_part2}")

if __name__ == "__main__":
    task_1()
    task_5()