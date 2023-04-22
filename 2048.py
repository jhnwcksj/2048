import tkinter
from tkinter import *
import random

number_color = {
2:      "#7a7167",
4:      "#7a7167",
8:      "#f7f4f0",
16:     "#f7f4f0",
32:     "#f7f4f0",
64:     "#f7f4f0",
128:    "#f7f4f0",
256:    "#f7f4f0",
512:    "#f7f4f0",
1024:   "#f7f4f0",
2048:   "#f7f4f0",
4096:   "#756d64",
8192:   "#f7f4f0",
16384:  "#756d64",
32768:  "#756d64",
65536:  "#f7f4f0",
}

cell_color = {
2:      "#ebe0d5",
4:      "#ebddc5",
8:      "#f0af78",
16:     "#f59462",
32:     "#f57a5d",
64:     "#f55e3b",
128:    "#ebcd71",
256:    "#ebca60",
512:    "#ebc650",
1024:   "#ebc33f",
2048:   "#edc22f",
4096:   "#ebe0d5",
8192:   "#edc22f",
16384:  "#edac74",
32768:  "#f59664",
65536:  "#f57c5f",
}

bind_escape = "Escape"
bind_back = "b"

bind_up = "Up"
bind_down = "Down"
bind_left = "Left"
bind_right = "Right"

bind_w = "w"
bind_s = "s"
bind_a = "a"
bind_d = "d"

bind_num8_up = "8"
bind_num5_down = "5"
bind_num4_left = "4"
bind_num6_right = "6"

# Логика матрицы
def new(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat



def result(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    for i in range(len(mat)-1):
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = []
    for j in range(4):
        partial_new = []
        for i in range(4):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done

# Логика движения

def up(game):
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done


def down(game):
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done


def left(game):
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done


def right(game):
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done

def gen():
    return random.randint(0, 3)

# Сама игра

class grid(Frame):
    def __init__(game):
        Frame.__init__(game)

        game.grid()
        game.master.title('2048')
        game.master.bind("<Key>", game.other_key)
        photo = tkinter.PhotoImage(file="2048.png")
        game.master.iconphoto(False, photo)
        game.master.resizable(False,False)
        game.master.geometry("+330+4")


# Команды движения
        game.commands = {
            bind_up: up,
            bind_down: down,
            bind_left: left,
            bind_right: right,
            bind_w: up,
            bind_s: down,
            bind_a: left,
            bind_d: right,
            bind_num8_up: up,
            bind_num5_down: down,
            bind_num4_left: left,
            bind_num6_right: right,


        }

        game.grid_cells = []
        game.cell_size()
        game.matrix = new(4)
        game.step = []
        game.new_cells()

        game.mainloop()

# Размер матрицы, текста и т.д
    def cell_size(game):
        background = Frame(game, bg="#91867c",width=400, height=400)
        background.grid()

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = Frame(
                    background,
                    bg="#998f85",
                    width=100,
                    height=100
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=7,
                    pady=7
                )
                t = Label(
                    master=cell,
                    text="",
                    bg="#998f85",
                    justify=CENTER,
                    font=("Verdana",55,"bold"),
                    width=4,
                    height=2)
                t.grid()
                grid_row.append(t)
            game.grid_cells.append(grid_row)


    def new_cells(game):
        for i in range(4):
            for j in range(4):
                new_number = game.matrix[i][j]
                if new_number == 0:
                    game.grid_cells[i][j].configure(text="",bg="#998f85")
                else:
                    game.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=cell_color[new_number],
                        fg=number_color[new_number]

                    )

        game.update_idletasks()


    def other_key(game, event):
        key = event.keysym
        print(event)
        if key == bind_escape: quit() # Команда для выхода вместо exit()
        if key == bind_back and len(game.step) > 1: # Команда для назад на 1 шаг
            game.matrix = game.step.pop()
            game.new_cells()
            print('back to :', len(game.step), 'step')
        elif key in game.commands:
            game.matrix, done = game.commands[key](game.matrix)
            # Результат игры
            if done:
                game.matrix = add_two(game.matrix)
                game.step.append(game.matrix)
                game.new_cells()
                if result(game.matrix) == 'win':
                    print("You Win!")
                    game.grid_cells[1][1].configure(text="You", bg="#998f85")
                    game.grid_cells[1][2].configure(text="Win!", bg="#998f85")
                if result(game.matrix) == 'lose':
                    print("You Lost!")
                    game.grid_cells[2][1].configure(text="You", bg="#998f85")
                    game.grid_cells[2][2].configure(text="Lost!", bg="#998f85")




    def next_matrix(game):
        index = (gen(), gen())
        while game.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        game.matrix[index[0]][index[1]] = 2



game_grid = grid()