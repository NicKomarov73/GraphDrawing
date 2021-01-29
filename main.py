from turtle import *
from tkinter import *
from tkinter import ttk
import random

window = Tk()
window.title("GraphDrawing")
window.configure(bd=10)
window.resizable(False, False)

colors = ["yellow", "green", "red", "blue"]
ver_size = [i for i in range(20, 80, 5)]
vertexs = []                            # [ [x, y, size, Vcolor, Tcolor] ]
selected = []
graph = []

def move(x, y, brus):
    brus.up()
    brus.goto(x, y)
    brus.down()

def check_circle(x, y):
    for num, ver in enumerate(vertexs):
        #ver[0] = x
        #ver[1] = y
        #ver[2] = radius
        if (x - ver[0])**2 + (y - ver[1])**2 <= ver[2]**2:
            return num
    return -1

def draw_ver(x, y, radius, ver_color, text_col, num, brus):
    move(x, y, brus)
    brus.pencolor(text_col)
    brus.dot(radius, ver_color)
    brus.write(num)

def highlight_ver(x, y, radius):
    move(x, y, brus)
    brus.pencolor('purple')
    brus.dot(radius)

def line(start, finish, col, brus):
    brus.pencolor(col)
    move(vertexs[start][0], vertexs[start][1], brus)
    brus.goto(vertexs[finish][0], vertexs[finish][1])

def clear():
    global brus
    move(-1000, -1000, brus)
    brus.dot(30000, 'white')
    graph.clear()
    vertexs.clear()
    selected.clear()

def delete_edge():
    global drus
    st = int(start_btn.get())-1
    fin = int(finish_btn.get())-1
    line(st, fin, 'white', brus)

def delete_ver(x, y):
    global brus
    if check_circle(x, y) != -1:

        num = check_circle(x, y)
        move(vertexs[num][0], vertexs[num][1], brus)
        brus.dot(vertexs[num][2], 'white')
        for count in graph[num]:
            v = vertexs[count]
            line(num, count, 'white', brus)
            draw_ver(v[0], v[1], v[2], v[3], v[4], count + 1, brus)
        vertexs.pop(num)
        graph.pop(num)

        for count, ver in enumerate(vertexs):
            draw_ver(ver[0], ver[1], ver[2], ver[3], ver[4], count+1, brus)

def generate_fun():
    global brus
    clear()
    v_count = int(Vcount.get())
    e_count = int(Ecount.get())

    while len(vertexs) < v_count:
        x = random.randint(-500, 500)
        y = random.randint(-400, 400)
        draw(x, y)

    while e_count > 0:
        fir = random.randint(0, v_count-1)
        sec = random.randint(0, v_count-1)
        line(fir, sec, 'black', brus)

        if not fir in graph[sec]:
            graph[sec].append(fir)
        if not sec in graph[fir]:
            graph[fir].append(sec)

        e_count -= 1

def draw(x, y):
    global brus
    ver_color = Vcolor.get()
    text_col = Tcolor.get()
    radius = int(Vsize.get())

    if check_circle(x, y) != -1:

        num = check_circle(x, y)
        if num in selected:
            selected.remove(num)
            draw_ver(vertexs[num][0], vertexs[num][1], radius, ver_color, text_col, num+1, brus)
        else:
            selected.append(num)
            highlight_ver(vertexs[num][0], vertexs[num][1], vertexs[num][2])

        if len(selected) == 2:
            line(selected[0], selected[1], 'black', brus)
            draw_ver(vertexs[selected[0]][0], vertexs[selected[0]][1], int(vertexs[selected[0]][2]), vertexs[selected[0]][3],
                     vertexs[selected[0]][4], selected[0] + 1, brus)
            draw_ver(vertexs[selected[1]][0], vertexs[selected[1]][1], int(vertexs[selected[1]][2]), vertexs[selected[1]][3],
                     vertexs[selected[1]][4], selected[1] + 1, brus)

            if not selected[1] in graph[selected[0]]:
                graph[selected[0]].append(selected[1])
            if not selected[0] in graph[selected[1]]:
                graph[selected[1]].append(selected[0])

            selected.clear()


    else:
        vertexs.append([x, y, radius, ver_color, text_col])
        graph.append([])
        draw_ver(x, y, radius, ver_color, text_col, len(vertexs), brus)



Vcolor = ttk.Combobox(window, width=40, values=colors)
Vcolor.current(0)
Vcolor.grid(column=0, row=0, sticky=W)

Tcolor = ttk.Combobox(window, width=40, values=colors)
Tcolor.current(2)
Tcolor.grid(column=0, row=1, sticky=W)

Vsize = ttk.Combobox(window, width=40, values=ver_size)
Vsize.current(2)
Vsize.grid(column=0, row=2, sticky=W)

start_btn = Entry(window)
start_btn.grid(column=1, row=0, sticky=W)

finish_btn = Entry(window)
finish_btn.grid(column=1, row=1, sticky=W)

del_btn = Button(window, width=16, text='DELETE', command=delete_edge)
del_btn.grid(column=1, row=2, sticky=W)

clear_btn = Button(window, width=16, text='CLEAR', command=clear)
clear_btn.grid(column=3, row=0, sticky=W)

Vcount = Entry(window)
Vcount.grid(column=2, row=0, sticky=W)

Ecount = Entry(window)
Ecount.grid(column=2, row=1, sticky=W)

generate_btn = Button(window, width=16, text='GENERATE', command=generate_fun)
generate_btn.grid(column=2, row=2, sticky=W)

canvas = Canvas(window, width=1200, height=900)
canvas.grid(column=0, row=3, columnspan=2)

draw_space = TurtleScreen(canvas)
#draw_space.bgcolor("black")
brus = RawTurtle(draw_space)
brus.hideturtle()
brus.speed(0)
draw_space.onscreenclick(draw, 1)
draw_space.onscreenclick(delete_ver, 3)

window.mainloop()