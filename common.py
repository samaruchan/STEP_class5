def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities

def read_output(filename):
    with open(filename) as f:
        tour = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            tour.append(int(line.replace('\n','')))
        return tour


def format_tour(tour):
    return 'index\n' + '\n'.join(map(str, tour))


def print_tour(tour):
    print(format_tour(tour))
