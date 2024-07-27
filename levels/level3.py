import heapq

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

def uniform_cost_search(n, m, t, f, map_data, start, goal):
    open_set = [(0, 0, start, f, [(start[0], start[1])])]
    visited = set()

    while open_set:
        time, cost, (x, y), fuel, path = heapq.heappop(open_set)

        if (x, y) == goal:
            return path if time <= t else []

        if (x, y, fuel) in visited:
            continue
        visited.add((x, y, fuel))

        for nx, ny in get_neighbors(x, y, n, m, map_data):
            new_time = time + 1
            new_cost = cost + 1
            new_fuel = fuel - 1

            cell = map_data[nx][ny]
            if cell.startswith('F'):
                refuel_time = int(cell[1:])
                new_time += refuel_time
                new_fuel = f
            elif cell.isdigit():
                new_time += int(cell)

            if new_fuel > 0 and new_time <= t:
                new_path = path + [(nx, ny)]
                heapq.heappush(open_set, (new_time, new_cost, (nx, ny), new_fuel, new_path))

    return []

def solve_level_3(n, m, t, f, map_data):
    start, goal = None, None
    for i in range(n):
        for j in range(m):
            if map_data[i][j] == 'S0':
                start = (i, j)
            elif map_data[i][j] == 'G0':
                goal = (i, j)

    if start and goal:
        path = uniform_cost_search(n, m, t, f, map_data, start, goal)
        return [path] if path else []
    return []

def level_3(input_file):
    from main import read_input
    n, m, t, f, map_data = read_input(input_file)

    # Solve the problem
    solution = solve_level_3(n, m, t, f, map_data)
    return map_data, solution