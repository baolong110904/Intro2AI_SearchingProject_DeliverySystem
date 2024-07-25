import level_1_search
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

def main():
  level_1()

if __name__ == '__main__':
  main()
