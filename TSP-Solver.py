import random
import math
import itertools
from typing import Tuple, Set, List
import time
import sys


def read_file(path: str):
    points = {}
    with open(path) as f:
        for line in f.readlines():
            try:
                ix, x, y = line.strip().split(' ')
                points[int(ix)] = (float(x), float(y))
            except ValueError:
                pass
    return points


def distance(point1: Tuple[float, float], point2: Tuple[float, float]):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def score(points: List[Tuple[float, float]]):
    return sum(distance(p1, p2) for p1, p2 in zip(points, points[1:] + [points[0]]))


def build_nn(points: Set[Tuple[float, float]]):
    points = points.copy()
    current = random.choice(tuple(points))
    result = []
    for _ in range(len(points)):
        result.append(current)
        points.remove(current)
        closest_point = None
        closest_distance = float("inf")
        for point in points:
            d = distance(current, point)
            if d < closest_distance:
                closest_distance = d
                closest_point = point
        current = closest_point
    return result


def two_opt_gain(points, i, j):
    size = len(points)
    prev_i = points[i]
    next_i = points[(i+1) % size]
    prev_j = points[j]
    next_j = points[(j+1) % size]
    old = distance(prev_i, next_i) + distance(prev_j, next_j)
    new = distance(prev_i, prev_j) + distance(next_i, next_j)
    return old - new


def two_opt(points: List[Tuple[float, float]]):
    candidates = (itertools.combinations(range(len(points)), 2))
    gains = ((two_opt_gain(points, i, j), i, j) for i, j in candidates if j - i > 2)
    best_gain, i, j = max(gains)
    if best_gain > 0:
        points[i+1:j+1] = points[i+1:j+1][::-1]
    return best_gain


TIME_LIMIT = 170

if __name__ == "__main__":
    start_time = time.time()
    file_name = sys.argv[1]
    print_score = len(sys.argv) > 2 and sys.argv[2] == "-s"
    id_to_point = read_file(file_name)
    point_to_id = {v: k for k, v in id_to_point.items()}
    points = set(id_to_point.values())
    best_tour = None
    best_score = float("inf")
    while time.time() - start_time <= TIME_LIMIT:
        tour_nn = build_nn(points)
        running_score = score(tour_nn)
        while time.time() - start_time <= TIME_LIMIT:
            gain = two_opt(tour_nn)
            if gain > 0:
                running_score -= gain
                if running_score < best_score:
                    best_tour = tour_nn.copy()
                    best_score = running_score
            else:
                break
    for point in best_tour:
        print(point_to_id[point], end=' ')
    print()
    if print_score:
        print(score(best_tour))
