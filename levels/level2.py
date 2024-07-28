import heapq
import ui

def read_input(file_path):
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]
    status = lines[0].split(' ')
    map = [[w for w in line.split(' ')] for line in lines[1:]]
    return *status, map

# UCS customized for lv2
def ucs_search_for_lv2(map, start, goal, t):
    rows, cols = len(map), len(map[0])
    queue = []
    heapq.heappush(queue, (0, start, [start]))
    costs = {start: 0}
    valid_paths = []
    while queue:
        cost, current, path = heapq.heappop(queue)
        if current == goal:
            if cost <= t:
                valid_paths.append(path)
            continue
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            if 0 <= next_row < rows and 0 <= next_col < cols:
                next_cell = map[next_row][next_col]
                if next_cell != '-1':
                    next_cost = cost + 1
                    if next_cell[0].isdigit():
                        next_cost += int(next_cell)
                    if (next_row, next_col) not in costs or next_cost < costs[(next_row, next_col)]:
                        costs[(next_row, next_col)] = next_cost
                        heapq.heappush(queue, (next_cost, (next_row, next_col), path + [(next_row, next_col)]))
    if valid_paths:
        return valid_paths
    else:
        return None

def calculate_time(map, path):
    time = 0
    for row, col in path[1:]:  # Skip the start position
        cell = map[row][col]
        time += 1  # Each step takes 1 minute
        if cell[0].isdigit():
            time += int(cell)  # Add toll booth time
    return time

def level_2(input_file):
    _, _, t, _, map = read_input(input_file)
    t = int(t)

    start, goal = None, None
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j].startswith('S0'):
                start = (i, j)
            elif map[i][j].startswith('G0'):
                goal = (i, j)
        if start != None and goal != None:
            break
    if start is None or goal is None:
        print("Invalid map, no start or goal found.")
        return
    solutions = ucs_search_for_lv2(map, start, goal, t)  
    if solutions:
        # Find the solution with the least time
        best_solution = min(solutions, key=lambda path: calculate_time(map, path))
        total_steps = len(best_solution) - 1  # Subtract 1 because the start position is included
        time_taken = calculate_time(map, best_solution)
    else:
        total_steps = 0
        time_taken = 0
    return map, [best_solution] if solutions else [], time_taken, total_steps