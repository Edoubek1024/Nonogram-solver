from random import randint
import time

GRID_HEIGHT = 10
GRID_WIDTH = 10
F_PERCENT = 60

colors = [
  "white", #white
  #"red", #red
  #"orange", #orange
  #"yellow", #yellow
  #"green", #green
  #"blue", #blue
  #"purple", #purple
  "black" #black
]


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


def new_grid():
  filler = GRID_HEIGHT*GRID_WIDTH*F_PERCENT // 100
  true_grid = [0 for i in range(0, GRID_HEIGHT*GRID_WIDTH)]
  while filler > 0:
    r = randint(0, len(true_grid) - 1)
    if true_grid[r] == 0:
      true_grid[r] = randint(1, len(colors) - 1)
      filler -= 1
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


def checker(g, t_g):
  for i in range(0, len(t_g)):
    if g[i] == len(colors) and t_g[i] == 0:
      continue
    if g[i] != t_g[i]:
      return False
  
  return True

def main():
  running = True
  
  grid, true_grid = new_grid()

  t = time.time()
  clues = 0

  while running:
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


if __name__ == "__main__":
  main()
  
