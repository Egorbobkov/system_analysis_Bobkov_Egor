from collections import deque, defaultdict

def build_relation_matrix(file_path: str, root_id: int):
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
        print("Ошибка: формат файла должен быть 'u,v' на строку.")
        return []

    if not edges:
        print("Файл пуст или не содержит корректных рёбер.")
        return []

    n = max(max(u, v) for u, v in edges)

    # непосредственное управление
    g1 = [[0] * n for _ in range(n)]
    for u, v in edges:
        g1[u - 1][v - 1] = 1

    # непосредственное подчинение
    g2 = [[g1[j][i] for j in range(n)] for i in range(n)]

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    # опосредованное управление/подчинение
    reachable = [[0] * n for _ in range(n)]
    for start in range(1, n + 1):
        visited = set()
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            for nxt in graph[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        for v in visited:
            reachable[start - 1][v - 1] = 1

    g3 = [[1 if reachable[i][j] and not g1[i][j] else 0 for j in range(n)] for i in range(n)]
    g4 = [[g3[j][i] for j in range(n)] for i in range(n)]

    # соподчинение
    level = {root_id: 0}
    queue = deque([root_id])
    while queue:
        cur = queue.popleft()
        for nxt in graph[cur]:
            level[nxt] = level[cur] + 1
            queue.append(nxt)

    g5 = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and level.get(i + 1) == level.get(j + 1):
                g5[i][j] = 1

    return g1, g2, g3, g4, g5


def main():
    file_path = input("Введите путь до csv-файла: ").strip()
    root_id = int(input("Введите номер корневого узла: ").strip())

    matrices = build_relation_matrix(file_path, root_id)

    if not matrices:
        return

    for idx, g in enumerate(matrices, 1):
        print(f"\nМатрица g{idx}:")
        for row in g:
            print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
