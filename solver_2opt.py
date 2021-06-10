#!/usr/bin/env python3

import sys
import math
import copy
import solver_greedy

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calculate_score(tour, dist, N):
    score = 0
    #insert dummy
    tour.append(tour[0])
    for i in range(N):
        score += dist[tour[i]][tour[i+1]]
    #delete dummy
    tour.pop()
    return score

def make_neighbor_tour(best_tour, dist, N):
    for i in range(1,N-1):
        for j in range(i+1, N):
            neighbor_tour = two_opt(i, j, best_tour)
            #insert dummy
            best_tour.append(best_tour[0])
            neighbor_tour.append(neighbor_tour[0])
            #calcurate score
            best_score = dist[best_tour[i-1]][best_tour[i]] + dist[best_tour[j]][best_tour[j+1]]
            neighbor_score = dist[neighbor_tour[i-1]][neighbor_tour[i]] + dist[neighbor_tour[j]][neighbor_tour[j+1]]
            #delete dummy
            best_tour.pop()
            neighbor_tour.pop()
            if neighbor_score < best_score:
                is_updated = True
                return neighbor_tour, is_updated

    is_updated = False   
    return best_tour, is_updated

def two_opt(i, j, tour):
    neighbor_tour = copy.deepcopy(tour)
    while (i < j):
        neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
        i+=1
        j-=1
    return neighbor_tour

def solve(cities):
    N = len(cities)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    #greedy
    best_tour = solver_greedy.solve(cities)
    best_score = calculate_score(best_tour, dist, N)
    print("greedy:{}".format(best_score))
    
    #2-opt
    is_updated = True
    while is_updated:
        is_updated = False
        neighbor_tour, is_updated = make_neighbor_tour(best_tour, dist, N)
        if is_updated:
            best_tour = copy.deepcopy(neighbor_tour)

    best_score = calculate_score(best_tour, dist, N)  
    print("greedy + 2_opt:{}".format(best_score))

    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)