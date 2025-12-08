import json
import sys


def main(json_str1, json_str2):
    ranking1 = json.loads(json_str1)
    ranking2 = json.loads(json_str2)

    objects = extract_objects(ranking1)
    matrix1 = build_matrix(ranking1, objects)
    matrix2 = build_matrix(ranking2, objects)

    contradictions = find_contradictions(matrix1, matrix2, objects)

    if contradictions:
        return json.dumps(contradictions)

    # Этап 2: если нет противоречий, возвращаем согласованную ранжировку
    # Для простоты берем более детальную ранжировку
    return json_str1 if is_more_detailed(ranking1, ranking2) else json_str2


def extract_objects(ranking):
    objects = []
    for item in ranking:
        if isinstance(item, list):
            objects.extend(item)
        else:
            objects.append(item)
    return objects


def build_matrix(ranking, objects):
    n = len(objects)
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    obj_to_cluster = {}
    cluster_index = 0

    # Определяем к какому кластеру относится каждый объект
    for cluster in ranking:
        if isinstance(cluster, list):
            cluster_items = cluster
        else:
            cluster_items = [cluster]

        for obj in cluster_items:
            obj_to_cluster[obj] = cluster_index
        cluster_index += 1

    # Заполняем матрицу
    for i in range(n):
        for j in range(n):
            obj_i = objects[i]
            obj_j = objects[j]

            # Объект i не хуже j, если его кластер левее или тот же
            if obj_to_cluster[obj_i] <= obj_to_cluster[obj_j]:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0

    for i in range(n):
        matrix[i][i] = 1

    return matrix


def find_contradictions(matrix1, matrix2, objects):
    n = len(objects)
    contradictions = []

    for i in range(n):
        for j in range(i + 1, n):
            # Противоречие: разные эксперты считают разных объект лучше
            if (matrix1[i][j] != matrix2[i][j]) or (matrix1[j][i] != matrix2[j][i]):
                pair = sorted([objects[i], objects[j]])
                if pair not in contradictions:
                    contradictions.append(pair)

    return contradictions


def is_more_detailed(ranking1, ranking2):
    # Более детальная ранжировка - та, где больше кластеров
    count1 = len(ranking1)
    count2 = len(ranking2)
    return count1 >= count2


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python task.py <json_str1> <json_str2>")
        sys.exit(1)

    result = main(sys.argv[1], sys.argv[2])
    print(result)