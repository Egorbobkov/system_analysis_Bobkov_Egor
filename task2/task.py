import sys
from math import log2
from collections import defaultdict, deque
from typing import Tuple, List, Set


def parse_edges(data: str) -> List[tuple]:
    edges = []
    for line in data.strip().splitlines():
        parts = [p.strip() for p in line.split(",") if p.strip()]
        if len(parts) > 1:
            edges.append((parts[0], parts[1]))
    return edges


def bfs_levels(graph, start):
    dist = {start: 0}
    q = deque([start])

    while q:
        node = q.popleft()
        for nei in graph[node]:
            if nei not in dist:
                dist[nei] = dist[node] + 1
                q.append(nei)

    return dist


def compute_entropy(edges: List[tuple], root: str) -> Tuple[float, float]:
    if not edges:
        return 0.0, 0.0

    nodes = sorted({a for a, b in edges} | {b for a, b in edges})
    n = len(nodes)

    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)

    levels = bfs_levels(g, root)

    R1 = set(edges)
    R2 = {(b, a) for a, b in edges}
    R3 = {(a, c) for (a, b) in edges for c in g[b] if (a, c) not in edges}
    R4 = {(x, y) for (y, x) in R3}
    R5 = {(a, b) for a in nodes for b in nodes if a != b and levels.get(a) == levels.get(b)}

    rel_sets: List[Set] = [R1, R2, R3, R4, R5]

    H = 0.0
    for node in nodes:
        for rel in rel_sets:
            cnt = sum(1 for (a, b) in rel if a == node)
            if cnt > 0:
                p = cnt / (n - 1)
                H += -p * log2(p)

    c = 0.53
    H_ref = c * n * len(rel_sets)
    H_norm = H / H_ref

    return round(H, 1), round(H_norm, 1)


def main():
    if len(sys.argv) < 3:
        print("Использование: python script.py файл.csv корень")
        sys.exit(1)

    file = sys.argv[1]
    root = sys.argv[2]

    with open(file, encoding="utf-8") as f:
        data = f.read()

    edges = parse_edges(data)
    h, norm = compute_entropy(edges, root)
    print((h, norm))
    return h, norm


if __name__ == "__main__":
    main()
