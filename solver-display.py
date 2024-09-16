import pygame
from random import randint
from pygame.locals import *
import time

GRID_HEIGHT = 8
GRID_WIDTH = 8
GRID_SIZE = 30
SPEED = float('inf')
F_PERCENT = 60

colors = [
  pygame.color.Color(255, 255, 255), #white
  #pygame.color.Color(255, 0, 0), #red
  #pygame.color.Color(255, 165, 0), #orange
  #pygame.color.Color(255, 255, 0), #yellow
  #pygame.color.Color(0, 255, 0), #green
  #pygame.color.Color(0, 0, 255), #blue
  #pygame.color.Color(128, 0, 128), #purple
  pygame.color.Color(0, 0, 0) #black
]


def init():
  global clock, screen
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((GRID_SIZE*(1.7*GRID_WIDTH + 1), GRID_SIZE*(1.7*GRID_HEIGHT + 1)), pygame.DOUBLEBUF)

def interpret(l):
  newl = []
  sum = 0
  for i in range(0, len(l)):
    if l[i] == 0 or l[i] == len(colors):
      continue
    sum += 1
    if i != (len(l) - 1) and l[i] == l[i + 1]:
      continue
    newl.append((l[i], sum))
    sum = 0

  return newl


def draw_handler(surface, grid, true_grid):
  COLOR = pygame.color.Color("white")
  surface.fill(COLOR)


  w_lists = [grid[i:i+GRID_WIDTH] for i in range(0, len(grid), GRID_WIDTH)]
  true_w_lists = [true_grid[i:i+GRID_WIDTH] for i in range(0, len(grid), GRID_WIDTH)]

  h_lists = []
  for i in range(0, GRID_WIDTH):
    new_h_list = [grid[i + j*GRID_WIDTH] for j in range(0, GRID_HEIGHT)]
    h_lists.append(new_h_list)
  true_h_lists = []
  for i in range(0, GRID_WIDTH):
    new_h_list = [true_grid[i + j*GRID_WIDTH] for j in range(0, GRID_HEIGHT)]
    true_h_lists.append(new_h_list)

  for i in range(0, GRID_HEIGHT):
    c_rect = pygame.Rect(GRID_WIDTH*GRID_SIZE, i*GRID_SIZE, GRID_SIZE, GRID_SIZE)
    l = interpret(w_lists[i])
    r_l = interpret(true_w_lists[i])
    if l == r_l:
      pygame.draw.rect(surface, pygame.color.Color(0,255,0), c_rect)
    else:
      pygame.draw.rect(surface, pygame.color.Color(255,255,255), c_rect)

  for i in range(0, GRID_WIDTH):
    c_rect = pygame.Rect(i*GRID_SIZE, GRID_HEIGHT*GRID_SIZE, GRID_SIZE, GRID_SIZE)
    l = interpret(h_lists[i])
    r_l = interpret(true_h_lists[i])
    if l == r_l:
      pygame.draw.rect(surface, pygame.color.Color(0,255,0), c_rect)
    else:
      pygame.draw.rect(surface, pygame.color.Color(255,255,255), c_rect)

  for x in range(0, GRID_SIZE*GRID_WIDTH, GRID_SIZE):
    for y in range(0, GRID_SIZE*GRID_HEIGHT, GRID_SIZE):
      c_rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
      cell_x = x // GRID_SIZE
      cell_y = y // GRID_SIZE
      block = cell_x + cell_y*GRID_WIDTH
      if grid[block] == len(colors):
        pygame.draw.rect(surface, pygame.color.Color(128, 128, 128), c_rect)
      else:
        pygame.draw.rect(surface, colors[grid[block]], c_rect)
      pygame.draw.rect(surface, pygame.color.Color("black"), c_rect, 2)

  for i in range(0, GRID_HEIGHT):
    if i % 5 == 0:
      pygame.draw.line(surface, pygame.color.Color(0, 0, 0), (0, GRID_SIZE*i), (GRID_SIZE*GRID_WIDTH, GRID_SIZE*i), 10)
  for i in range(0, GRID_WIDTH):
    if i % 5 == 0:
      pygame.draw.line(surface, pygame.color.Color(0, 0, 0), (GRID_SIZE*i, 0), (GRID_SIZE*i, GRID_SIZE*GRID_HEIGHT), 10)

  down = 0
  for i in true_w_lists:
    texts = interpret(i)
    dis = GRID_SIZE*(GRID_WIDTH + 1)
    for j in texts:
      pointfont = pygame.font.Font(None, GRID_SIZE)
      text = pointfont.render(f"{j[1]}", True, colors[j[0]])
      text_rect = text.get_rect()
      text_rect.center = (dis + (GRID_SIZE // 2), (GRID_SIZE // 2) + (GRID_SIZE*down))
      surface.blit(text, text_rect)
      dis += GRID_SIZE*.6
    down += 1

  up = 0
  for i in true_h_lists:
    texts = interpret(i)
    dis = GRID_SIZE*(GRID_HEIGHT + 1)
    for j in texts:
      pointfont = pygame.font.Font(None, GRID_SIZE)
      text = pointfont.render(f"{j[1]}", True, colors[j[0]])
      text_rect = text.get_rect()
      text_rect.center = ((GRID_SIZE // 2) + (GRID_SIZE*up), dis + (GRID_SIZE // 2))
      surface.blit(text, text_rect)
      dis += GRID_SIZE*.6
    up += 1

def new_grid():
  def fix_whites(grid):
    for i in range(0, len(grid)):
      if grid[i] >= len(colors):
        grid[i] = 0
  true_grid = [randint(1, round((len(colors)-1)*(1/(F_PERCENT/100)))) for i in range(0, GRID_HEIGHT*GRID_WIDTH)]
  fix_whites(true_grid)
  grid = [0 for i in range(0, GRID_HEIGHT*GRID_WIDTH)]
  return grid, true_grid

def give_pos(l, need, current):

  def all_bins(lis, depth, hints, big_list, hint, current):
      
      if len(lis) == len(current) and hint == len(hints):
        big_list.append(list(lis)) 
        return
      elif len(lis) > len(current):
        return
    
      new_list = list(lis) 
    
      new_list.append(0) 
      if len(current) >= len(new_list) and (current[len(new_list) - 1] == len(colors) or current[len(new_list) - 1] == 0): 
        zero = all_bins(new_list, (depth + 1), hints, big_list, hint, current) 
    
      new_list.pop()
      if hint >= len(hints):
        return
      for i in range(0, hints[hint][1]):
        new_list.append(hints[hint][0])
        if len(current) < len(new_list) or (current[len(new_list) - 1] != 0 and new_list[-1] != current[len(new_list) - 1]): 
          return
      if len(hints) > hint + 1 and hints[hint][0] == hints[hint + 1][0]: 
        new_list.append(len(colors))
        if len(current) < len(new_list) or (current[len(new_list) - 1] != 0 and new_list[-1] != current[len(new_list) - 1]): 
          return
      
      one = all_bins(new_list, (depth + 1), hints, big_list, hint + 1, current)
      
  real_possibilities = []
  zeros = []
  all_bins(zeros, 0, l, real_possibilities, 0, current)
  
  test = list(current)
  for i in real_possibilities:
    for j in range(0, len(test)):
      if (test[j] == len(colors) or test[j] == 0) and i[j] == 0:
        test[j] = len(colors)
        continue
      if test[j] == 0:
        test[j] = i[j]
        continue
      if test[j] != i[j]:
        test[j] = -1
  
  for i in range(0, len(test)):
    if test[i] == -1:
      test[i] = 0
    elif test[i] == 0:
      test[i] = len(colors)
      
  return test

def ai_run(grid, true_grid, clue):
  grid_check = list(grid)
  w_lists = [grid[i:i+GRID_WIDTH] for i in range(0, len(grid), GRID_WIDTH)]
  true_w_lists = [true_grid[i:i+GRID_WIDTH] for i in range(0, len(grid), GRID_WIDTH)]

  h_lists = []
  for i in range(0, GRID_WIDTH):
    new_h_list = [grid[i + j*GRID_WIDTH] for j in range(0, GRID_HEIGHT)]
    h_lists.append(new_h_list)
  true_h_lists = []
  for i in range(0, GRID_WIDTH):
    new_h_list = [true_grid[i + j*GRID_WIDTH] for j in range(0, GRID_HEIGHT)]
    true_h_lists.append(new_h_list)

  for i in range(0, len(true_w_lists)):
    g = give_pos(interpret(true_w_lists[i]), GRID_WIDTH, w_lists[i])
    for j in range(0, GRID_WIDTH):
      if grid[j + GRID_WIDTH*i] == 0:
        grid[j + GRID_WIDTH*i] = g[j]

  for i in range(0, len(h_lists)):
    g = give_pos(interpret(true_h_lists[i]), GRID_HEIGHT, h_lists[i])
    for j in range(0, GRID_HEIGHT):
      if grid[i + GRID_WIDTH*j] == 0:
        grid[i + GRID_WIDTH*j] = g[j]
        
  if grid_check == grid:
    blanks = []
    for i in range(0, len(grid)):
      if grid[i] == 0:
        blanks.append(i)
    r = blanks[randint(0, len(blanks) - 1)]
    if true_grid[r] == 0:
      grid[r] = len(colors)
    else:
      grid[r] = true_grid[r]
    return (clue + 1)
  else:
    return clue

def change_cell(grid, x, y, GRID_HEIGHT, GRID_WIDTH):
  cell_x = x // GRID_SIZE
  cell_y = y // GRID_SIZE
  if cell_x > GRID_WIDTH or cell_y > GRID_HEIGHT:
    return
  grid[cell_x + cell_y*GRID_WIDTH] = (grid[cell_x + cell_y*GRID_WIDTH] + 1) % (len(colors) + 1)
  
  return

def checker(g, t_g):
  for i in range(0, len(t_g)):
    if g[i] == len(colors) and t_g[i] == 0:
      continue
    if g[i] != t_g[i]:
      return False
  
  return True

def main():
  init()
  model = [(0, 0)]
  running = True
  auto = False

  grid, true_grid = new_grid()

  t = time.time()
  clues = 0

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEMOTION:
        model.pop()
        model.append(event.pos)
      elif event.type == pygame.MOUSEBUTTONUP and not auto:
        change_cell(grid, event.pos[0], event.pos[1], GRID_HEIGHT, GRID_WIDTH)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
        auto = not auto
        t = time.time()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        grid = [0 for i in range(0, len(true_grid))]
      elif event.type == pygame.KEYDOWN:
        pass
    if auto:
      clues = ai_run(grid, true_grid, clues)
    if checker(grid, true_grid):
      grid, true_grid = new_grid()
      t = time.time() - t
      if clues == 0:
        print(f"{round(t, 5)} s SOLVED")
      elif clues == 1:
        print(f"{round(t, 5)} s SOLVED (1 hint needed)")
      else:
        print(f"{round(t, 5)} s SOLVED ({clues} hints needed)")
      clues = 0
      t = time.time()
    draw_handler(screen, grid, true_grid)
    pygame.display.flip()
    clock.tick(SPEED)


if __name__ == "__main__":
  main()
  
