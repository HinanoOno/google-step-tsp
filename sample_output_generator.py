#!/usr/bin/env python3

from common import format_tour, read_input

import solver_greedy
import solver_random
import main

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in ((solver_random, 'random'), (solver_greedy, 'greedy')):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')

    #test3 outputのファイルを生成
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = main.solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
