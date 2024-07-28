import pygame
import itertools
import math
COLORS = {
  "t": (0, 0, 0), # Black
  '0': (255, 255, 255), # White
  '-1': (121, 121, 121), # Gray
  "n": (100, 116, 139), # Slate 
  **dict.fromkeys(['S', 'G', 'S0', 'G0'], (239, 68, 68)), # Red
  **dict.fromkeys(['S1', 'G1'], (234, 88, 12)), # Orange
  **dict.fromkeys(['S2', 'G2'], (245, 158, 11)), # Yellow
  **dict.fromkeys(['S3', 'G3'], (132, 204, 22)), # Lime
  **dict.fromkeys(['S4', 'G4'], (22, 163, 74)), # Green
  **dict.fromkeys(['S5', 'G5'], (6, 128, 212)), # Cyan
  **dict.fromkeys(['S6', 'G6'], (59, 130, 246)), # Blue
  **dict.fromkeys(['S7', 'G7'], (139, 92, 246)), # Violet
  **dict.fromkeys(['S8', 'G8'], (168, 85, 247)), # Purple
  **dict.fromkeys(['S9', 'G9'], (236, 72, 153)), # Pink
  'F': (244, 63, 94), # Rose
}

# UI
def draw_cell(surface, map, pos):
    row, col = pos
    cell = map[row][col]
    color, text = None, None
    # Color
    if cell.isnumeric() and cell != '0' and cell != '-1':
        color = COLORS["n"]
    elif cell.startswith('F'):
        color = COLORS['F']
    else:
        color = COLORS.get(cell, COLORS['0'])  # Default to white if color not found
    # Text
    if cell != '0' and cell != '-1':
        text = pygame.font.SysFont('Arial', 20).render(cell, True, COLORS["t"])
    # Draw
    pygame.draw.rect(surface, color, pygame.Rect(50*col, 50*row, 49, 49))
    if text:
        surface.blit(text, (50*col + 25 - text.get_width()/2, 50*row + 25 - text.get_height()/2))
        
def draw_path(surface, pos, next_pos, agent):
  if not pos or not next_pos or pos == next_pos: return
  row, col = pos
  next_row, next_col = next_pos
  # Path direction
  path = None
  if row == next_row:
    if col < next_col: path = pygame.Rect(50*col + (25-2), 50*row + (25-2), 50, 4)
    else: path = pygame.Rect(50*col - (25-2), 50*row + (25-2), 50, 4)
  else:
    if row < next_row: path = pygame.Rect(50*col + (25-2), 50*row + (25-2), 4, 50)
    else: path = pygame.Rect(50*col + (25-2), 50*row - (25-2), 4, 50)
  # Draw
  pygame.draw.rect(surface, COLORS[agent], path)

def draw_info_panel(surface, time_taken, total_steps):
    panel_width = 200
    panel_height = surface.get_height()
    panel_rect = pygame.Rect(surface.get_width() - panel_width, 0, panel_width, panel_height)
    
    # Draw panel background
    pygame.draw.rect(surface, COLORS['n'], panel_rect)
    pygame.draw.line(surface, COLORS['t'], (panel_rect.left, 0), (panel_rect.left, panel_height), 2)
    
    # Draw info text
    font = pygame.font.SysFont('Arial', 24)
    time_text = font.render(f"Time: {time_taken} minutes", True, COLORS['0'])
    steps_text = font.render(f"Steps: {total_steps}", True, COLORS['0'])
    
    surface.blit(time_text, (panel_rect.left + 10, 20))
    surface.blit(steps_text, (panel_rect.left + 10, 60))  

def ui(caption, map, solution, time_taken, total_steps):
    # Calculate new surface size
    map_width = 50 * len(map[0])
    map_height = 50 * len(map)
    panel_width = 200
    surface_width = map_width + panel_width
    surface_height = max(map_height, 200)  # Ensure minimum height for info panel
    
    # Init surface
    pygame.init()
    pygame.display.set_caption(caption)
    surface = pygame.display.set_mode((surface_width, surface_height))

    # Draw map
    for row in range(len(map)):
        for col in range(len(map[0])):
            draw_cell(surface, map, (row, col))
    
    # Draw info panel
    draw_info_panel(surface, time_taken, total_steps)
    
    pygame.display.update()
    
    # Wait before start
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN: break

    if solution:
        # Draw paths
        agent_num = len(solution)
        max_steps = max(len(path) for path in solution)
        for step in range(max_steps - 1):  # -1 to avoid going out of bounds
            pygame.time.delay(500)
            for i, path in enumerate(solution):
                if step < len(path) - 1:  # Check if there's a next step for this agent
                    current_pos = path[step]
                    next_pos = path[step + 1]
                    draw_path(surface, current_pos, next_pos, f'G{i}')
            pygame.display.update()
    
    # Wait before quit
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN: break
    pygame.quit()


def draw_button(surface, text, position, size):
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, COLORS['n'], button_rect)
    pygame.draw.rect(surface, COLORS['t'], button_rect, 2)
    font = pygame.font.SysFont('Arial', 24)
    text_surf = font.render(text, True, COLORS['t'])
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    return button_rect

def draw_background(screen):
    background = pygame.Surface(screen.get_size())
    for y in range(screen.get_height() - 160):
        color = (max(0, min(255, 200 - y // 3)), max(0, min(255, 220 - y // 3)), max(0, min(255, 255 - y // 3)))
        pygame.draw.line(background, color, (0, y), (screen.get_width(), y))
    return background

def level_selection():
    pygame.init()
    screen = pygame.display.set_mode((600, 850))
    pygame.display.set_caption("Delivery System")
    clock = pygame.time.Clock()

    # Background
    background = draw_background(screen)

    # Fonts
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 36)

    # Title
    title = title_font.render("Delivery System", True, (30, 30, 100))
    title_shadow = title_font.render("Delivery System", True, (100, 100, 150))

    # Buttons
    button_size = (250, 80)
    buttons = [
        {
            'rect': pygame.Rect((175, 350 + i*90), button_size),
            'color': (220, 220, 220),
            'text': f"Level {i}",
            'hover': False
        } for i in range(1, 5)
    ]

    # Car animation
    car_img = pygame.image.load('ui/car.png').convert_alpha()
    truck_img = pygame.image.load('ui/truck.png').convert_alpha()
    car_img = pygame.transform.scale(car_img, (60, 60))
    truck_img = pygame.transform.scale(truck_img, (80, 80))
    car_left_to_right = {'x': -60, 'speed': 1.5}
    truck_right_to_left = {'x': 660, 'speed': -1.25}

    def draw_button(button, screen):
        color = button['color']
        if button['hover']:
            color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        pygame.draw.rect(screen, color, button['rect'], border_radius=15)
        pygame.draw.rect(screen, (100, 100, 150), button['rect'], 3, border_radius=15)
        
        text = button_font.render(button['text'], True, (30, 30, 80))
        text_rect = text.get_rect(center=button['rect'].center)
        screen.blit(text, text_rect)

    animation_time = 0
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Animate and center title
        title_y = 50 + math.sin(animation_time * 0.05) * 5
        title_x = (600 - title.get_width()) // 2
        screen.blit(title_shadow, (title_x + 2, title_y + 2))
        screen.blit(title, (title_x, title_y))

        # Draw road
        pygame.draw.rect(screen, (100, 100, 100), (0, 200, 600, 60))
        pygame.draw.rect(screen, (255, 255, 0), (0, 228, 600, 4))

        # Animate cars
        car_left_to_right['x'] += car_left_to_right['speed']
        if car_left_to_right['x'] > 600:
            car_left_to_right['x'] = -60

        truck_right_to_left['x'] += truck_right_to_left['speed']
        if truck_right_to_left['x'] < -60:
            truck_right_to_left['x'] = 660

        screen.blit(car_img, (car_left_to_right['x'], 208))
        screen.blit(truck_img, (truck_right_to_left['x'], 152))

        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            button['hover'] = button['rect'].collidepoint(mouse_pos)
            draw_button(button, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button['rect'].collidepoint(event.pos):
                        return i + 1

        animation_time += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_button(screen, text, pos, size, font):
    button_rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, (220, 220, 220), button_rect, border_radius=15)
    pygame.draw.rect(screen, (100, 100, 150), button_rect, 3, border_radius=15)
    
    text_surface = font.render(text, True, (30, 30, 80))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_button(screen, text, pos, size, font):
    button_rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, (220, 220, 220), button_rect, border_radius=15)
    pygame.draw.rect(screen, (100, 100, 150), button_rect, 3, border_radius=15)
    
    text_surface = font.render(text, True, (30, 30, 80))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def algorithm_selection():
    pygame.init()
    screen = pygame.display.set_mode((600, 850))
    pygame.display.set_caption("Algorithm Selection")
    clock = pygame.time.Clock()
    background = draw_background(screen)

    algorithms = [
        "Breadth-First Search",
        "Depth-First Search",
        "Uniform-Cost Search",
        "Greedy Best First Search",
        "A* Search"
    ]

    button_size = (300, 50)
    button_font = pygame.font.Font(None, 36)
    
    buttons = [
        draw_button(screen, alg, (150, 150 + i * 70), button_size, button_font)
        for i, alg in enumerate(algorithms)
    ]

    pygame.display.flip()

    running = True
    while running:
        screen.blit(background, (0, 0))
        
        for i, alg in enumerate(algorithms):
            button = buttons[i]
            draw_button(screen, alg, (150, 150 + i * 70), button_size, button_font)

        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                draw_button(screen, algorithms[i], (150, 150 + i * 70), button_size, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        return i

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
def input_selection():
    pygame.init()
    screen = pygame.display.set_mode((600, 850))
    pygame.display.set_caption("Input Selection")
    clock = pygame.time.Clock()
    background = draw_background(screen)

    inputs = [f"Input {i}" for i in range(1, 6)]

    button_size = (300, 50)
    button_font = pygame.font.Font(None, 36)
    
    buttons = [
        draw_button(screen, inp, (150, 150 + i * 70), button_size, button_font)
        for i, inp in enumerate(inputs)
    ]

    pygame.display.flip()

    running = True
    while running:
        screen.blit(background, (0, 0))
        
        for i, inp in enumerate(inputs):
            button = buttons[i]
            draw_button(screen, inp, (150, 150 + i * 70), button_size, button_font)

        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                draw_button(screen, inputs[i], (150, 150 + i * 70), button_size, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        return i + 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()