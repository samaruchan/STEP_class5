#!/usr/bin/env python3

import sys
import math
import random, copy
from common import format_tour, read_input, read_output
#Simulated Annealing
TEMPERATURE = 2500
MAXITER = 20000
ALPHA = 0.99
#solve
#if challenge5 or challenge6: recommend COUNT > 100
#else: COUNT > 1 
COUNT = 100


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calculate_score(tour, dist, N):
    score = 0
    #insert dummy
    tour.append(tour[0])
    for i in range(N):
        score += dist[tour[i]][tour[i+1]]
    tour.pop()
    return score

def get_neighbor_tour_by_2opt(tour, score, dist, N):
    is_updated = False
    #choose two  random points
    i = random.randrange(N - 1)
    j = i + random.randrange(N - i)

    neighbor_tour = two_opt(i, j, tour)

    #calculate score
    if j == N - 1:
        temp_score = dist[tour[i-1]][tour[i]] + dist[tour[j]][tour[0]]
        temp_neighbor_score = dist[neighbor_tour[i-1]][neighbor_tour[i]] + dist[neighbor_tour[j]][neighbor_tour[0]]
        neighbor_score = score - temp_score + temp_neighbor_score        
    else:
        temp_score = dist[tour[i-1]][tour[i]] + dist[tour[j]][tour[j+1]]
        temp_neighbor_score = dist[neighbor_tour[i-1]][neighbor_tour[i]] + dist[neighbor_tour[j]][neighbor_tour[j+1]]
        neighbor_score = score - temp_score + temp_neighbor_score

    if neighbor_score < score:
        is_updated = True

    return neighbor_tour, neighbor_score, is_updated

def two_opt(i, j, tour):
    neighbor_tour = copy.deepcopy(tour)
    while (i < j):
        neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
        i+=1
        j-=1
    return neighbor_tour

def get_neighbor_tour_by_3opt(tour, score, dist, N):
    is_updated = False

    #choose two  random points   
    i = random.randrange(N)
    while True:        
        j = random.randrange(N)
        if  j == i or j == (i - 1) % N:
            # neighbor_tour == tour
            pass
        else:
            # neighbor_tour != tour
            break
    
    neighbor_tour = three_opt(i, j, tour, N)

    #calcurate score
    if j == N - 1:
        temp_score = dist[tour[i-1]][tour[i]] + dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[0]]
        temp_neighbor_score = dist[tour[i-1]][tour[i+1]] + dist[tour[j]][tour[i]] + dist[tour[i]][tour[0]]
        neighbor_score = score - temp_score + temp_neighbor_score        
    elif i == N - 1:
        temp_score = dist[tour[i-1]][tour[i]] + dist[tour[i]][tour[0]] + dist[tour[j]][tour[j+1]]
        temp_neighbor_score = dist[tour[i-1]][tour[0]] + dist[tour[j]][tour[i]] + dist[tour[i]][tour[j+1]]
        neighbor_score = score - temp_score + temp_neighbor_score
    else:
        temp_score = dist[tour[i-1]][tour[i]] + dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]
        temp_neighbor_score = dist[tour[i-1]][tour[i+1]] + dist[tour[j]][tour[i]] + dist[tour[i]][tour[j+1]]
        neighbor_score = score - temp_score + temp_neighbor_score
    
    if neighbor_score < score:
        is_updated = True

    return neighbor_tour, neighbor_score, is_updated

def three_opt(i, j, tour, N):
    neighbor_tour = []
    for k in range(N):
        if k == i:
            pass
        else:
            neighbor_tour.append(tour[k])
        if k == j:
            neighbor_tour.append(tour[i])
    return neighbor_tour

def calculate_energy(score, neighbor_score, iter):
    if score >= neighbor_score:
        return 1
    else:
        t = ALPHA**(iter / MAXITER)
        return math.exp((score - neighbor_score) / t)

def updated_best_tour(tour, score):
    best_score = score
    best_tour = copy.deepcopy(tour)

    return best_tour, best_score

#Simulated Annealing
def solve_by_2opt(tour, score, dist, N):
    best_tour = copy.deepcopy(tour)
    best_score = score

    for iter in range(MAXITER):
        neighbor_tour, neighbor_score, is_updated = get_neighbor_tour_by_2opt(tour, score, dist, N)
        if is_updated:
            best_score = neighbor_score
            best_tour = copy.deepcopy(neighbor_tour)
        if random.random() < calculate_energy(score, neighbor_score, iter):
            tour = copy.deepcopy(neighbor_tour)
            score = neighbor_score

    return best_tour, best_score

#Simulated Annealing
def solve_by_3opt(tour, score, dist, N):
    best_tour = copy.deepcopy(tour)
    best_score = score

    for iter in range(MAXITER):
        neighbor_tour, neighbor_score, is_updated = get_neighbor_tour_by_3opt(tour, score, dist, N)
        if is_updated:
            best_score = neighbor_score
            best_tour = copy.deepcopy(neighbor_tour)
        if random.random() < calculate_energy(score, neighbor_score, iter):
            tour = copy.deepcopy(neighbor_tour)
            score = neighbor_score

    return best_tour, best_score

def solve(cities, output):
    N = len(cities)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    best_tour = read_output(output)
    best_score = calculate_score(best_tour, dist, N)
    print("score0: {}".format(best_score))

    for num in range(10):
        #init tour
        tour = copy.deepcopy(best_tour)
        for i in range(N):
            j = random.randrange(N)
            tour[i], tour[j] = tour[j], tour[i]
        score = calculate_score(tour, dist, N)

        #solve tsp
        for _ in range(COUNT):
            tour, score = solve_by_2opt(tour, score, dist, N)
            if score < best_score:
                best_tour, best_score = updated_best_tour(tour, score)
        for _ in range(COUNT):
            tour, score = solve_by_3opt(tour, score, dist, N)
            if score < best_score:
                best_tour, best_score = updated_best_tour(tour, score)
        
        print("score{}: {}".format(num + 1, score))
    
    return best_tour, best_score

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    output = sys.argv[2]
    best_tour, best_score = solve(cities, output)
    with open(output, 'w') as f:
        f.write(format_tour(best_tour) + '\n')
    print("best score: {}".format(best_score))
    