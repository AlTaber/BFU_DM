import sys
import os
from collections import Counter


def read_text_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    with open(filepath, 'r', encoding="utf-8") as f:
        return f.read()


def analyze_characters(text: str) -> Counter:
    return Counter(text)


def analyze_bigrams(text: str) -> Counter:
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    return Counter(bigrams)


def escape_char(char: str) -> str:
    special = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\\': '\\\\',
        ' ': '\\s',  # пробел тоже экранируем для однозначности
    }

    if char in special:
        return special[char]

    # Непечатаемые символы -> \xHH
    if not char.isprintable():
        return '\\x{:02x}'.format(ord(char))

    return char


def escape_bigram(bigram: str) -> str:
    return escape_char(bigram[0]) + escape_char(bigram[1])


def save_analysis(text: str, output_path: str):
    total_chars = len(text)

    if total_chars == 0:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Empty file\n")
        return

    char_freq = analyze_characters(text)
    bigram_freq = analyze_bigrams(text)
    total_bigrams = sum(bigram_freq.values())

    with open(output_path, 'w', encoding='utf-8') as f:
        # Заголовок с метаданными
        f.write(f"# total_chars={total_chars}\n")
        f.write(f"# unique_chars={len(char_freq)}\n")
        f.write(f"# total_bigrams={total_bigrams}\n")
        f.write(f"# unique_bigrams={len(bigram_freq)}\n")
        f.write(f"# format: item<TAB>count<TAB>probability\n")
        f.write("\n")

        # Секция символов
        f.write("=== CHARS ===\n")
        for char, count in char_freq.most_common():
            probability = count / total_chars
            escaped = escape_char(char)
            f.write(f"{escaped}\t{count}\t{probability:.10f}\n")

        f.write("\n")

        # Секция биграмм
        f.write("=== BIGRAMS ===\n")
        for bigram, count in bigram_freq.most_common():
            probability = count / total_bigrams
            escaped = escape_bigram(bigram)
            f.write(f"{escaped}\t{count}\t{probability:.10f}\n")

    print(f"Анализ сохранён: {output_path}")
    print(f"  Символов: {len(char_freq)} уникальных из {total_chars} всего")
    print(f"  Биграмм:  {len(bigram_freq)} уникальных из {total_bigrams} всего")


def main():
    # Путь к входному файлу
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Путь к .txt файлу: ").strip().strip('"').strip("'")

    # Путь к выходному файлу
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        base = os.path.splitext(filepath)[0]
        output_path = f"{base}_freq.txt"

    try:
        text = read_text_file(filepath)
        save_analysis(text, output_path)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()