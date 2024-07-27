import ui
from levels import level1 
from levels import level2 
from levels import level3  

def read_input(file_path):
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]
    n, m, t, f = map(int, lines[0].split(' '))
    map_data = [line.split(' ') for line in lines[1:]]
    return n, m, t, f, map_data

def main():
    selected_level = ui.level_selection()
    if selected_level is None:
        return

    if selected_level == 1:
        selected_algorithm = ui.algorithm_selection()
        if selected_algorithm is None:
            return
        map_data, solution = level1.level_1('input/input_level_1.txt', selected_algorithm)
        ui.ui(f"Level {selected_level}", map_data, solution)
    elif selected_level == 2:
        map_data, solution = level2.level_2('input/input_level_2.txt')
        ui.ui(f"Level {selected_level}", map_data, solution)
    elif selected_level == 3:
        map_data, solution = level3.level_3('input/input_level3_1.txt')
        ui.ui(f"Level {selected_level}", map_data, solution)
    elif selected_level == 4:
        # Implement Level 4
        pass

if __name__ == '__main__':
    main()
