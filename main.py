import level_1_search
import level_2_search
import ui

# Input
def read_input(file_path):
  with open(file_path) as file:
    lines = [line.rstrip() for line in file]
  status = [int(n) for n in lines[0].split(' ')]
  map = [[w for w in line.split(' ')] for line in lines[1:]]
  return *status, map
  
# Levels
def level_1():
  w, h, map = read_input('input_level_1.txt')
  bfs_solution = level_1_search.breath_first_search(w, h, map)
  ui.ui("Level 1 - Breath-First Search", map, [bfs_solution])
  dfs_solution = level_1_search.depth_first_search(w, h, map)
  ui.ui("Level 1 - Depth-First Search", map, [dfs_solution])
  ucs_solution = level_1_search.uniform_cost_search(w, h, map)
  ui.ui("Level 1 - Uniform-cost Search", map, [ucs_solution])
  gbfs_solution = level_1_search.greedy_best_first_search(w, h, map)
  ui.ui("Level 1 - Greedy Best-first Search", map, [gbfs_solution])
  as_solution = level_1_search.a_start_search(w, h, map)
  ui.ui("Level 1 - A* Search", map, [as_solution])

def level_2():
    _, _, t, _, map = read_input('input_level_2.txt')
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
    solutions = level_2_search.ucs_search_for_lv2(map, start, goal, t)
    if solutions:
        ui.ui("Level 2", map, [solutions[0]])
    else:
        print("No path found within the committed delivery time.")
def main():
  # level_1()
  level_2()

if __name__ == '__main__':
  main()
