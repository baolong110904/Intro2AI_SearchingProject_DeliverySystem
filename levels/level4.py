import heapq
import random

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_valid_move(x, y, n, m, map_data):
    return 0 <= x < n and 0 <= y < m and map_data[x][y] != '-1'

def get_neighbors(x, y, n, m, map_data):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(nx, ny, n, m, map_data):
            neighbors.append((nx, ny))
    return neighbors

def a_star_level4(n, m, t, f, map_data, start, goal, other_vehicles):
    open_set = [(0, 0, start, f, [start])]
    visited = set()

    while open_set:
        _, time, current, fuel, path = heapq.heappop(open_set)

        if current == goal:
            return path

        if (current, fuel) in visited:
            continue
        visited.add((current, fuel))

        cx, cy = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if not is_valid_move(nx, ny, n, m, map_data) or (nx, ny) in other_vehicles:
                continue

            new_time = time + 1
            new_fuel = fuel - 1
            cell = map_data[nx][ny]
            
            if cell.startswith('T'):
                new_time += int(cell[1:])
            elif cell.startswith('F'):
                new_time += int(cell[1:])
                new_fuel = f

            if new_time <= t and new_fuel >= 0:
                new_path = path + [(nx, ny)]
                heapq.heappush(open_set, (new_time + heuristic((nx, ny), goal), new_time, (nx, ny), new_fuel, new_path))

    return None

def random_des(n, m, map_data, occupied_cells):
    while True:
        x, y = random.randint(0, n-1), random.randint(0, m-1)
        if map_data[x][y] != '-1' and (x, y) not in occupied_cells:
            return (x, y)

def solve_level_4(n, m, t, f, map_data):
    vehicles = []
    goals = {}
    max_goal_index = 0

    for i in range(n):
        for j in range(m):
            cell = map_data[i][j]
            if cell == 'S':
                vehicles.append((i, j))
            elif cell.startswith('S'):
                index = int(cell[1:])
                vehicles.append((i, j))
                if index > max_goal_index:
                    max_goal_index = index
            elif cell == 'G':
                goals[0] = (i, j)
            elif cell.startswith('G'):
                index = int(cell[1:])
                goals[index] = (i, j)

    paths = [[start] for start in vehicles]
    turns = 0
    
    while turns <= t:
        occupied_cells = set(vehicles)
        for i, vehicle in enumerate(vehicles):
            if i == 0 and vehicle == goals.get(0):
                return paths

            if goals.get(i) is None:
                goals[i] = random_des(n, m, map_data, occupied_cells)

            other_vehicles = vehicles[:i] + vehicles[i+1:]
            path = a_star_level4(n, m, t, f, map_data, vehicle, goals[i], set(other_vehicles))

            if path and len(path) > 1:
                vehicles[i] = path[1]
                paths[i].append(path[1])
            else:
                paths[i].append(vehicle)
        
        turns += 1

    return paths

def level_4(input_file):
    from main import read_input
    n, m, t, f, map_data = read_input(input_file)

    solution = solve_level_4(n, m, t, f, map_data)
    time_taken = max(len(path) for path in solution)
    total_steps = sum(len(path) for path in solution)
    
    return map_data, solution, time_taken, total_steps