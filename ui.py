import pygame
import itertools

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
  **dict.fromkeys([f'F{i}' for i in range(10)], (244, 63, 94)), # Rose
}

# UI
def draw_cell(surface, map, pos):
  row, col = pos
  cell = map[row][col]
  color, text = None, None
  # Color
  if cell.isnumeric() and cell != '0' and cell != -1: color = COLORS["n"]
  else: color = COLORS[cell]
  # Text
  if cell != '0' and cell != '-1':text = pygame.font.SysFont('Arial', 20).render(cell, True, COLORS["t"])
  # Draw
  pygame.draw.rect(surface, color, pygame.Rect(50*col, 50*row, 49, 49))
  if text: surface.blit(text, (50*col + 25 - text.get_width()/2, 50*row + 25 - text.get_height()/2))
  
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
  
def ui(caption, map, solution):
  # Init surface
  pygame.init()
  pygame.display.set_caption(caption)
  surface = pygame.display.set_mode((500, 500))

  # Draw map
  for row in range(len(map)):
    for col in range(len(map[0])):
      draw_cell(surface, map, (row, col))
  pygame.display.update()
  
  # Wait before start
  pygame.event.clear()
  while True:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN: break
  
  # Draw paths
  agent_num = len(solution)
  steps = [step for step in itertools.chain(*itertools.zip_longest(*solution))]
  for i in range(len(steps) - agent_num): # Skip start and goal
    if not i % agent_num: pygame.time.delay(200)
    draw_path(surface, steps[i], steps[i + agent_num], f'G{i % agent_num}')
    pygame.display.update()
    
  # Wait before quit
  pygame.event.clear()
  while True:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN: break
  pygame.quit()
