import json
import sys


def main(json_str1, json_str2):
    ranking1 = json.loads(json_str1)
    ranking2 = json.loads(json_str2)

    parsed1 = parse_ranking(ranking1)
    parsed2 = parse_ranking(ranking2)

    all_objects = sorted(extract_objects(parsed1) | extract_objects(parsed2))
    comparison = build_comparison_matrix(all_objects, parsed1, parsed2)
    consensus = find_consensus(all_objects, comparison)

    return json.dumps(consensus)


def parse_ranking(ranking):
    """Преобразует ранжировку в список кластеров"""
    parsed = []
    for item in ranking:
        if isinstance(item, list):
            parsed.append([str(x) for x in item])
        else:
            parsed.append([str(item)])
    return parsed


def extract_objects(parsed_ranking):
    """Извлекает все объекты из ранжировки"""
    objects = set()
    for cluster in parsed_ranking:
        objects.update(cluster)
    return objects


def compare_objects(obj1, obj2, ranking):
    """Сравнивает два объекта в ранжировке"""
    pos1 = pos2 = None

    for i, cluster in enumerate(ranking):
        if obj1 in cluster:
            pos1 = i
        if obj2 in cluster:
            pos2 = i

    if pos1 is None or pos2 is None:
        return 0

    if pos1 < pos2:
        return 1
    elif pos1 > pos2:
        return -1
    else:
        return 0


def build_comparison_matrix(objects, r1, r2):
    """Строит матрицу согласованных сравнений"""
    n = len(objects)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            comp1 = compare_objects(objects[i], objects[j], r1)
            comp2 = compare_objects(objects[i], objects[j], r2)

            if comp1 == comp2:
                matrix[i][j] = comp1
            elif comp1 == 0:
                matrix[i][j] = comp2
            elif comp2 == 0:
                matrix[i][j] = comp1
            elif comp1 == -comp2:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 0

    return matrix


def find_consensus(objects, comparison):
    """Находит согласованную кластерную ранжировку"""
    n = len(objects)
    visited = [False] * n
    clusters = []

    for i in range(n):
        if visited[i]:
            continue

        cluster = [i]
        visited[i] = True

        for j in range(n):
            if not visited[j]:
                # Проверяем, равны ли объекты
                if comparison[i][j] == 0 and comparison[j][i] == 0:
                    # Проверяем транзитивность
                    valid = True
                    for k in cluster:
                        if comparison[k][j] != 0 or comparison[j][k] != 0:
                            valid = False
                            break
                    if valid:
                        cluster.append(j)
                        visited[j] = True

        clusters.append(cluster)

    m = len(clusters)
    graph = [[] for _ in range(m)]
    indegree = [0] * m

    for i in range(m):
        for j in range(m):
            if i == j:
                continue

            # Проверяем, что все объекты из i лучше всех из j
            i_better = True
            for idx_i in clusters[i]:
                for idx_j in clusters[j]:
                    if comparison[idx_i][idx_j] != 1:
                        i_better = False
                        break
                if not i_better:
                    break

            if i_better:
                graph[i].append(j)
                indegree[j] += 1

    # Топологическая сортировка
    from collections import deque
    queue = deque([i for i in range(m) if indegree[i] == 0])
    sorted_clusters = []

    while queue:
        current = queue.popleft()
        sorted_clusters.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    result = []
    for cluster_idx in sorted_clusters:
        cluster_objects = [objects[idx] for idx in clusters[cluster_idx]]

        formatted = []
        for obj in sorted(cluster_objects):
            try:
                formatted.append(int(obj))
            except ValueError:
                formatted.append(obj)

        if len(formatted) == 1:
            result.append(formatted[0])
        else:
            result.append(sorted(formatted))

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python task.py '<ранжировка1>' '<ранжировка2>'")
        sys.exit(1)

    json_str1 = sys.argv[1]
    json_str2 = sys.argv[2]

    # Убираем лишние кавычки
    if (json_str1.startswith("'") and json_str1.endswith("'")) or \
            (json_str1.startswith('"') and json_str1.endswith('"')):
        json_str1 = json_str1[1:-1]

    if (json_str2.startswith("'") and json_str2.endswith("'")) or \
            (json_str2.startswith('"') and json_str2.endswith('"')):
        json_str2 = json_str2[1:-1]

    result = main(json_str1, json_str2)
    print(result)