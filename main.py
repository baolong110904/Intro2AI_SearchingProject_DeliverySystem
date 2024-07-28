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

    selected_algorithm = None
    if selected_level == 1:
        selected_algorithm = ui.algorithm_selection()
        if selected_algorithm is None:
            return

    selected_input = ui.input_selection()
    if selected_input is None:
        return

    input_file = f'input/input{selected_input}_level_{selected_level}.txt'

    if selected_level == 1:
        map_data, solution, time_taken, total_steps = level1.level_1(input_file, selected_algorithm)
        ui.ui(f"Level {selected_level}", map_data, solution, time_taken, total_steps)
    elif selected_level == 2:
        map_data, solution, time_taken, total_steps = level2.level_2(input_file)
        ui.ui(f"Level {selected_level}", map_data, solution, time_taken, total_steps)
    elif selected_level == 3:
        map_data, solution, time_taken, total_steps = level3.level_3(input_file)
        ui.ui(f"Level {selected_level}", map_data, solution, time_taken, total_steps)
    elif selected_level == 4:
        # Implement Level 4
        pass

if __name__ == '__main__':
    main()