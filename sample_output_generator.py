#!/usr/bin/env python3

from common import format_tour, read_input, read_output
import solver_sa

CHALLENGES = 7

def generate_output():
    for i in range(CHALLENGES):
        print("CHALLENGES{}".format(i))
        cities = read_input(f'input_{i}.csv')
        output = f'output_{i}.csv'
        best_tour, best_score = solver_sa.solve(cities, output)
        with open(output, 'w') as f:
            f.write(format_tour(best_tour) + '\n')
        print("best score: {}".format(best_score))


if __name__ == '__main__':
    generate_output()

