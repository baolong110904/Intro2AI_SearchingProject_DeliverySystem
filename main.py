import ui

# Input
def read_input(file_path):
  with open(file_path) as file:
    lines = [line.rstrip() for line in file]
  status = lines[0].split(' ')
  map = [[w for w in line.split(' ')] for line in lines[1:]]
  return *status, map
  
# Levels
def level_4():
  _, _, _, _, map = read_input('input_level_4.txt')
  
  # TODO: solve problem
  solution = [
    [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (6,2), (6,3), (5,3), (5,4), (5,5), (6,5), (7,5), (7,6), (7,7), (7,8)],
    [(2,5), (3,5), (4,5), (5,5), (5,4), (5,3), (6,3), (7,3), (7,2), (6,2), (6,1), (6,0), (7,0), (8,0), (9,0)],
    [(8,5), (7,5), (6,5), (6,5), (6,5), (6,5), (5,5), (4,5), (4,6)]
  ]
  
  # Display
  ui.ui("Level 4", map, solution)

def main():
  level_4()

if __name__ == '__main__':
  main()
