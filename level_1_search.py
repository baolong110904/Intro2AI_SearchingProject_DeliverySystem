def read_map(w, h, map):
  start = [(i, j) for i in range(w) for j in range(h) if map[i][j] == 'S'][0]
  goal = [(i, j) for i in range(w) for j in range(h) if map[i][j] == 'G'][0]
  return start, goal

def get_path(moves: list[tuple[int, int]]):
  moves.reverse()
  path = [*moves[0]]
  for fr, to in moves:
    if to == path[0]:
      path.insert(0, fr)
  return path

def breath_first_search(w, h, map):
  start, goal = read_map(w, h, map)
  if start == goal: return [start]
  frontier, reached, moves = [start], [start], []
  # Loop
  while frontier:
    node = frontier.pop(0)
    # Expand
    children = [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]
    for child in children:
      if child[0] in range(0, w) and child[1] in range(0, h) and child not in reached and map[child[0]][child[1]] != "-1":
        if child == goal: return get_path([*moves, (node, child)])
        moves.append((node, child))
        reached.append(child)
        frontier.append(child)
  return reached

def depth_first_search(w, h, map):
  start, goal = read_map(w, h, map)
  if start == goal: return [start]
  frontier, reached, moves = [start], [start], []
  # Loop
  while frontier:
    node = frontier.pop()
    # Expand
    children = [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]
    for child in children:
      if child[0] in range(0, w) and child[1] in range(0, h) and child not in reached and map[child[0]][child[1]] != "-1":
        if child == goal: return get_path([*moves, (node, child)])
        moves.append((node, child))
        reached.append(child)
        frontier.append(child)
  return []

def uniform_cost_search(w, h, map):
  start, goal = read_map(w, h, map)
  if start == goal: return [start]
  frontier, cost, expanded, moves = [start], [0], [start], []
  # Loop
  while len(frontier):
    # Pick the min cost node
    min_cost = min(cost)
    node = frontier.pop(cost.index(min_cost))
    cost.remove(min_cost)
    expanded.append(node)
    # Expand
    if node == goal: return get_path(moves[0:len(moves) - [m[1] for m in moves][::-1].index(node)])
    children = [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]
    for child in children:
      if child[0] in range(0, w) and child[1] in range(0, h) and child not in expanded and map[child[0]][child[1]] != "-1":
        child_cost = min_cost + 1
        if child not in frontier:
          frontier.append(child)
          cost.append(child_cost)
          moves.append((node, child))
        elif child_cost < cost[frontier.index(child)]:
          cost[frontier.index(child)] = child_cost
          moves.append((node, child))
  return []
        
def greedy_best_first_search(w, h, map):
  start, goal = read_map(w, h, map)
  if start == goal: return [start]
  frontier, reached, moves = [start], [start], []
  # Loop
  while len(frontier):
    # Pick the min heuristic node
    node = min([(abs(n[0] - goal[0]) + abs(n[1] - goal[1]) , n) for n in frontier])[1]
    frontier.remove(node)
    # Expand
    children = [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]
    for child in children:
      if child[0] in range(0, w) and child[1] in range(0, h) and child not in reached and map[child[0]][child[1]] != "-1":
        if child == goal: return get_path([*moves, (node, child)])
        moves.append((node, child))
        reached.append(child)
        frontier.append(child)
  return reached

def a_start_search(w, h, map):
  start, goal = read_map(w, h, map)
  if start == goal: return [start]
  frontier, cost, expanded, moves = [start], [abs(start[0] - goal[0]) + abs(start[1] - goal[1])], [start], []
  # Loop
  while len(frontier):
    # Pick the min cost node
    min_cost = min(cost)
    node = frontier.pop(cost.index(min_cost))
    cost.remove(min_cost)
    expanded.append(node)
    # Expand
    if node == goal: return get_path(moves[0:len(moves) - [m[1] for m in moves][::-1].index(node)])
    children = [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]
    for child in children:
      if child[0] in range(0, w) and child[1] in range(0, h) and child not in expanded and map[child[0]][child[1]] != "-1":
        child_cost = min_cost - (abs(node[0] - goal[0]) + abs(node[1] - goal[1])) + 1 + (abs(child[0] - goal[0]) + abs(child[1] - goal[1]))
        if child not in frontier:
          frontier.append(child)
          cost.append(child_cost)
          moves.append((node, child))
        elif child_cost < cost[frontier.index(child)]:
          cost[frontier.index(child)] = child_cost
          moves.append((node, child))
  return []