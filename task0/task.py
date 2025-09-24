def build_matrix_adjacency(file_path: str):
    edges = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                u, v = map(int, line.strip().split(","))
                edges.append((u, v))
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден")
        return []
    except ValueError:
        print("Ошибка: проверь формат файла (должно быть 'u,v' на строку).")
        return []

    if not edges:
        print("Файл пуст или не содержит корректных рёбер")
        return []

    n = max(max(u, v) for u, v in edges)
    matrix = [[0] * n for _ in range(n)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1
        matrix[v - 1][u - 1] = 1

    return matrix


def main():
    file_path = input("Введите путь до csv-файла: ").strip()
    matrix = build_matrix_adjacency(file_path)

    if matrix:
        print("Матрица смежности:")
        for row in matrix:
            print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
