from collections import Counter
from functools import lru_cache
import sys

sys.setrecursionlimit(5000)


def task_1():
    source_word = "ЧЕРЕСПОЛОСИЦА"
    target_length = 5
    
    letter_counts = Counter(source_word)
    
    unique_words = set()

    def backtrack(current_word):
        if len(current_word) == target_length:
            unique_words.add(current_word)
            return

        for char in letter_counts:
            if letter_counts[char] > 0:
                letter_counts[char] -= 1
                
                backtrack(current_word + char)
                
                letter_counts[char] += 1

    backtrack("")
    print(f"Задание 1: Количество различных слов = {len(unique_words)}")

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