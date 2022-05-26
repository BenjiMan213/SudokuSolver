import pygame, sys
from pygame.locals import *
# pygame and sys for visual demonstration of how the board is solved
import numpy
# numpy for random number generation used only for generating randomized boards


def has_dupes(l): #returns true if the list l has any numbers between 1 and 9 (inclusive) that reoccur, false otherwise
    for i in range(1, 10):
        if l.count(i) <= 1:
            continue
        else:
            return True
    return False

def flip_board(board): #returns the transpose of the given 9x9 list board
    l = []
    for i in range(len(board)):
        l.append([board[t][i] for t in range(len(board))])
    return l

def block_board(board): #returns a list containing the values contained within each of the 9 3x3 blocks in the 9x9 list board
    inc = [0,3,6]
    new_board = [[] for _ in range(9)]
    index_1 = 0
    index_2 = 0
    for p in range(9):
        if p%3 == 0 and not p == 0:
            index_2 = 0
            index_1 += 3
        for t in range(3):
            for i in range(3):
                new_board[p].append(board[index_1+t][index_2+i])
        index_2 += 3
    return new_board

def is_valid(board): #returns false if any of the sudoku rules of recurrance have been violated, true otherwise
    l = len(board)
    for t in range(l):
        if has_dupes(board[t]):
            return False
        elif has_dupes(flip_board(board)[t]):
            return False
        elif has_dupes(block_board(board)[t]):
            return False
    return True

def is_complete(board): #returns false if there are any empty spaces in the board, true otherwise (empty space denoted by 0)
    for i in board:
        if 0 in i:
            return False
    return True

def is_solved(board): #returns true if the board is in a state that has been solved
    return is_complete(board) and is_valid(board)

def swap_rows(board, x, y): #swaps rows x and y in the board
    temp = [i for i in board[x]]
    board[x] = board[y]
    board[y] = temp
    
def swap_triple_rows(board, x, y): #swaps rows from x to x + 3 with rows y to y + 3 respectively
    for i in range(3):
        swap_rows(board, x * 3 + i, y * 3 + i)
        
def swap_columns(board, x, y): #swaps columns x and y in the board
    temp = [board[i][x] for i in range(9)]
    for i in range(9):
        board[i][x] = board[i][y]
        board[i][y] = temp[i]

def swap_triple_columns(board, x, y): #swaps columns from x to x+3 with columns y to y+3 respectively
    for i in range(3):
        swap_columns(board, x * 3 + i, y * 3 + i)

def randomized_board(): #returns a complete randomly generated sudoku board
    board = [[4, 3, 1, 6, 7, 9, 5, 2, 8],
             [9, 6, 7, 2, 5, 8, 3, 4, 1],
             [5, 8, 2, 1, 4, 3, 9, 6, 7],
             [6, 5, 9, 8, 1, 7, 2, 3, 4],
             [3, 2, 8, 5, 6, 4, 1, 7, 9],
             [7, 1, 4, 9, 3, 2, 8, 5, 6],
             [8, 7, 3, 4, 2, 1, 6, 9, 5],
             [1, 4, 5, 3, 9, 6, 7, 8, 2],
             [2, 9, 6, 7, 8, 5, 4, 1, 3]]
    for i in range(10):
        method = np.random.randint(1,5)
        if method == 1:
            x = np.random.randint(9)
            swap_rows(board, x,
                      np.random.choice([int(x/3)*3 + (x-2)%3, int(x/3)*3 + (x-1)%3]))
        elif method == 2:
            x = np.random.randint(9)
            swap_columns(board, x,
                         np.random.choice([int(x/3)*3 + (x-2)%3, int(x/3)*3 + (x-1)%3]))
        elif method == 3:
            x = np.random.randint(3)
            swap_triple_rows(board, x,
                             np.random.choice([int(x/3)*3 + (x-2)%3, int(x/3)*3 + (x-1)%3]))
        elif method == 4:
            x = np.random.randint(3)
            swap_triple_columns(board, x,
                                np.random.choice([x//3*3 + (x-2)%3, x//3*3 + (x-1)%3]))
        return board
            
def unsolved_board(missing_pieces): #returns a randomly generated sudoku board with a variable number of missing spaces (missing_pieces)
    coords = []
    board = randomized_board()
    for i in range(missing_pieces):
        coords.append([np.random.randint(9), np.random.randint(9)])
    for t in coords:
        board[t[0]][t[1]] = 0
    return board

def empty_spaces(board): #returns (row, column) coordinates of every empty space in the board
    coords = []
    for i in range(9):
        for t in range(9):
            if board[i][t] == 0:
                coords.append([i, t])
    return coords
    
def not_in_row(l, k): #returns all the values in list l that are not in list k
    uncommon = []
    for i in range(len(l)):
        if l[i] not in k:
            uncommon.append(l[i])
    return uncommon

def possibilities(board, empty): #returns a list of all valid values for each empty space in the board at the given state of the board
    n_list = []
    flipped = flip_board(board)
    blocked = block_board(board)
    for i in empty:
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        number_list = not_in_row(number_list, board[i[0]])
        number_list = not_in_row(number_list, flipped[i[1]])
        index = block_coords(i)
        number_list = not_in_row(number_list, blocked[index])
        n_list.append(number_list)
    eliminate_row(n_list, empty)
    eliminate_col(n_list, empty)
    return n_list

def remove_from_list(l, num): #removes num from the list l if it exists
    if num in l:
        l.pop(index_of(l, num))
    
def row_possibilities(possible, coords, row): #returns a concatenated list of all the possible values for every empty space in the given row
    l = []
    for i in range(len(possible)):
        if coords[i][0] == row:
            for t in possible[i]:
                l.append(t)
    return l

def col_possibilities(possible, coords, col): #returns a concatenated list of all the possible values for every empty space in the given column
    l = []
    for i in range(len(possible)):
        if coords[i][1] == col:
            for t in possible[i]:
                l.append(t)
    return l

#eliminates num from the every possible value for every empty space in the given block except for
#those in the given row if row=True, otherwise it does the same but with a column being the exception
def eliminate_from_block(possible, coords, block, exception, num, row): 
    for i in range(len(possible)):
        if block_coords(coords[i]) == block and not coords[i][0] == exception and row:
            remove_from_list(possible[i], num)
        elif block_coords(coords[i]) == block and not coords[i][1] == exception and not row:
            remove_from_list(possible[i], num)
        
def eliminate_row(possible, coords): #eliminates values from rows using the Candidate Lines technique used for solving sudoku
    arr = []
    for i in range(9):
        arr.append([])
        possibilities = row_possibilities(possible, coords, i)
        for t in range(1, 10):
            arr[-1].append(possibilities.count(t))
    new_arr = []
    
    for i in range(9):
        new_arr.append([])
        for t in range(1, 10):
            if arr[i][t-1] < 4 and arr[i][t-1] > 0:
                new_arr[-1].append(t)
    new_new_arr = []
    for i in range(9):
        new_new_arr.append([])
        for t in new_arr[i]:
            counter = 0
            for _ in possible:
                if coords[counter][0] == i and t in _:
                    break
                counter += 1
            block = block_coords(coords[counter])
            eliminate = True
            for e in range(len(possible)):
                if coords[e][0] == i and t in possible[e]:
                    if not block == block_coords(coords[e]):
                        eliminate = False
                    block = block_coords(coords[e])
            if eliminate:
                new_new_arr[-1].append([t, block])
    
    for i in range(len(new_new_arr)):
        for t in new_new_arr[i]:
            eliminate_from_block(possible, coords, t[1], i, t[0], True)

def eliminate_col(possible, coords): #eliminates values from columns using the Candidate Lines technique used for solving sudoku
    arr = []
    for i in range(9):
        arr.append([])
        possibilities = col_possibilities(possible, coords, i)
        for t in range(1, 10):
            arr[-1].append(possibilities.count(t))
    new_arr = []
    
    for i in range(9):
        new_arr.append([])
        for t in range(1, 10):
            if arr[i][t-1] < 4 and arr[i][t-1] > 0:
                new_arr[-1].append(t)
    new_new_arr = []
    for i in range(9):
        new_new_arr.append([])
        for t in new_arr[i]:
            counter = 0
            for _ in possible:
                if coords[counter][1] == i and t in _:
                    break
                counter += 1
            block = block_coords(coords[counter])
            eliminate = True
            for e in range(len(possible)):
                if coords[e][1] == i and t in possible[e]:
                    if not block == block_coords(coords[e]):
                        eliminate = False
                    block = block_coords(coords[e])
            if eliminate:
                new_new_arr[-1].append([t, block])
                
    for i in range(len(new_new_arr)):
        for t in new_new_arr[i]:
            eliminate_from_block(possible, coords, t[1], i, t[0], False)
            
def index_of(arr, x): #returns the index of x in the list arr
    counter = 0
    for i in arr:
        if i == x:
            break
        counter += 1
    return counter

def hidden_rows(possible, coords): #returns values that appear only once in all the possible values for their empty spaces in their respective rows
    l = [i for i in possible]
    for i in range(len(possible)):
        for t in range(len(possible)):
            if coords[t][0] == coords[i][0] and not t == i:
                l[i] = not_in_row(l[i], possible[t])
    return l

def hidden_cols(possible, coords): #returns values that appear only once in all the possible values for their empty spaces in their respective columns
    l = [i for i in possible]
    for i in range(len(possible)):
        for t in range(len(possible)):
            if coords[t][1] == coords[i][1] and not t == i:
                l[i] = not_in_row(l[i], possible[t])
    return l

def block_coords(coords): #given the (row, column) coordinates of a cell, returns which block that cell would be in
    index = coords[0] - coords[0] % 3 + coords[1] // 3
    return index

def hidden_blocks(possible, coords): #returns values that appear only once in all the possible values for their empty spaces in their respective blocks
    l = [i for i in possible]
    for i in range(len(possible)):
        for t in range(len(possible)):
            if block_coords(coords[t]) == block_coords(coords[i]) and not t == i:
                l[i] = not_in_row(l[i], possible[t])
    return l

def fill_hidden(board, possible, empty): #fills values into empty spaces using the Hidden Singles used for solving sudoku
    global display_surface, size, positions, FPS, text_color, bg_color
    hidden = [hidden_rows(possible, empty), hidden_cols(possible, empty),
              hidden_blocks(possible, empty)]
    # [rows, columns, blocks]
    for i in hidden:
        for t in range(len(empty)):
            if len(i[t]) == 1:
                board[empty[t][0]][empty[t][1]] = i[t][0]
                display_surface.blit(font.render(str(i[t][0]), True, text_color, bg_color),
                                     positions[empty[t][0]][empty[t][1]])
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                FramePerSec.tick(FPS)

def fill(board): #fills values into empty spaces using the Naked Singles technique used for solving sudoku
    global display_surface, size, FPS, positions, text_color, bg_color
    coords = empty_spaces(board)
    possible_vals = possibilities(board, coords)
    lengths = [len(i) for i in possible_vals]
    for i in range(len(coords)):
        if len(possible_vals[i]) == 1:
            board[coords[i][0]][coords[i][1]] = possible_vals[i][0]
            display_surface.blit(font.render(str(possible_vals[i][0]), True, text_color, bg_color),
                                 positions[coords[i][0]][coords[i][1]])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            FramePerSec.tick(FPS)
    fill_hidden(board, possible_vals, coords)
    
def print_notes(coords, possible_vals): #prints all the possible values of every empty space in the same format as the 9x9 board
    arr = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
    for i in range(len(coords)):
        arr[coords[i][0]][coords[i][1]] = possible_vals[i]
    for i in arr:
        print('')
        for t in i:
            if type(t) == list:
                for _ in t:
                    print(_, end='')
                print(".", end='')
                print(" " * (9 - len(t)), end='')
            else:
                print('-', " " * 8, end= '')

def solve_board(board): #recursive helper function used to solve the sudoku using previous functions and backtracking
    global display_surface, size, FPS, text_color, bg_color
    temp1 = [[t for t in i] for i in board]
    temp = [[t for t in i] for i in temp1]
    while not is_solved(temp1):
        temp = [[t for t in i] for i in temp1]
        fill(temp1)
        if not is_valid(temp1):
            break
        if temp == temp1:
            temp1 = backtrack(temp1)
            break
    if is_solved(temp1):
        texts = [[[font.render("" if temp1[i][t] == 0 else str(temp1[i][t]), True, text_color, bg_color),
                   (size // 18 + t * size // 9 - 5, size // 9 * i + 10)] for t in range(9)]for i in range(0,9)]
        for i in texts:
            for t in i:
                display_surface.blit(t[0], t[1])
            FramePerSec.tick(FPS)
        return temp1
    else:
        return temp

def backtrack(board): #recursive helper function used to solve the sudoku using previous functions and backtracking
    global display_surface, size, positions, FPS, text_color, bg_color
    coords = empty_spaces(board)
    possible_vals = possibilities(board, coords)
    lengths = [len(i) for i in possible_vals]
    if 0 in lengths:
        return board
    min_index = index_of(lengths, min(lengths))
    board_copy = [[t for t in i] for i in board]
    for i in possible_vals[min_index]:
        board_copy[coords[min_index][0]][coords[min_index][1]] = i
        print("1", end='')
        display_surface.blit(font.render(str(i), True, text_color, bg_color), positions[coords[min_index][0]][coords[min_index][1]])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        FramePerSec.tick(FPS)
        board_copy = solve_board(board_copy)
        if is_solved(board_copy):
            return board_copy
        else:
            board_copy = [[t for t in i] for i in board]
            texts = [[[font.render("0" if board[i][t] == 0 else str(board[i][t]), True, bg_color if board[i][t] == 0 else text_color, bg_color), (size // 18 + t * size // 9 - 5, size // 9 * i + 10)] for t in range(9)]for i in range(0,9)]
            for i in texts:
                for t in i:
                    display_surface.blit(t[0], t[1])
                FramePerSec.tick(FPS)
            
    return board

def print_board(board, disp, text_col=(0,0,0), bg_col=(255,255,255),size=500):
    texts = [[[font.render("" if board[i][t] == 0 else str(board[i][t]), True, text_col, bg_col), (size // 18 + t * size // 9 - 5, size // 9 * i + 10)] for t in range(9)]for i in range(0,9)]
    for i in texts:
        for t in i:
            disp.blit(t[0], t[1])


#initializing supposedly the hardest sudoku puzzle so far for the program to solve
board = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 3, 6, 0, 0, 0, 0, 0],
         [0, 7, 0, 0, 9, 0, 2, 0, 0],
         [0, 5, 0, 0, 0, 7, 0, 0, 0],
         [0, 0, 0, 0, 4, 5, 7, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 3, 0],
         [0, 0, 1, 0, 0, 0, 0, 6, 8],
         [0, 0, 8, 5, 0, 0, 0, 1, 0],
         [0, 9, 0, 0, 0, 0, 4, 0, 0]] 


#initializing the program
pygame.init()
font = pygame.font.SysFont('Arial',35)
 
# assigning a framerate, raise FPS to solve faster
FPS = 1000
FramePerSec = pygame.time.Clock()
 
# Configuring all the colors that will be used
white = (255, 255, 255)
black = (0,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0,0,255)

text_color = black
bg_color = yellow
background = yellow
grid_color = black
 
# setting up a square display with a caption
size = 600
display_surface = pygame.display.set_mode((size, size))
display_surface.fill(background)
pygame.display.set_caption("SUDOKU SOLVER")
 
#drawing the grid
def draw_grid(display_surface):
    global size, grid_color
    for i in range(1,9):
        pygame.draw.line(display_surface, grid_color,  (i * size//9, 0), (i * size // 9, size))
        pygame.draw.line(display_surface, grid_color, (0, i * size // 9), (size, i * size // 9))
    for i in range(1, 3):
        pygame.draw.line(display_surface, grid_color, (i * size//3, 0), (i * size // 3, size), width=3)
        pygame.draw.line(display_surface, grid_color, (0, i * size // 3), (size, i * size // 3), width=3)

draw_grid(display_surface)
#to keep track of the positions of each number in the pygame window
positions = [[(size // 18 + t * size // 9 - 5, size // 9 * i + 10) for t in range(9)]for i in range(0,9)]

#print the initial numbers of the board
print_board(board, display_surface, size=size, text_col=text_color, bg_col=bg_color)

pygame.display.update()
pygame.time.wait(2000)

#beginning the loop that solves the list board and the pygame board
board = solve_board(board)

display_surface.fill(green)
print_board(board, display_surface, size=size, text_col=black, bg_col=green)
draw_grid(display_surface)

#game loop for after the puzzle is solved, press x to exit
while True:
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    FramePerSec.tick(FPS)
