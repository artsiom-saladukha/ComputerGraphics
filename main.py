import time
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def draw_pixel(graph, x, y, color):
    x_draw = [x, x + 1]
    y_draw = [y, y + 1]
    graph.plot(x_draw, y_draw, color=color)


def dda_algorithm(graph, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if dx == 0 and dy == 0:
        draw_pixel(graph, x1, y1, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for _ in range(steps):
        draw_pixel(graph, round(x), round(y), color)
        x += x_inc
        y += y_inc


def bresenham_algorithm(graph, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if x1 > x2:
        sx = -1
    else:
        sx = 1
    if y1 > y2:
        sy = -1
    else:
        sy = 1

    if dx > dy:
        err = dx / 2.0
        while x1 != x2:
            draw_pixel(graph, x1, y1, color)
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
    else:
        err = dy / 2.0
        while y1 != y2:
            draw_pixel(graph, x1, y1, color)
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy


def castle_pitway_algorithm(graph, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    diff = dy > dx

    if diff:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    y = y1

    for x in range(x1, x2 + 1):
        if diff:
            draw_pixel(graph, y, x, color)
        else:
            draw_pixel(graph, x, y, color)

        error -= dy
        if error < 0:
            y += ystep
            error += dx


def draw_smooth_line(graph, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    diff = dy > dx

    if diff:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    y = y1

    for x in range(x1, x2 + 1):
        if diff:
            draw_pixel_with_smooth(graph, y, x, color, error / dx)
        else:
            draw_pixel_with_smooth(graph, x, y, color, error / dx)

        error -= dy
        if error < 0:
            y += ystep
            error += dx


def draw_pixel_with_smooth(graph, x, y, color, opacity):
    current_color = graph.get_pixel_color(x, y)
    smoothed_color = interpolate_color(current_color, color, opacity)
    draw_pixel(graph, x, y, smoothed_color)


def interpolate_color(color1, color2, factor):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return r, g, b


root = tk.Tk()
fig = plt.figure()
graph = fig.add_subplot(111)
plt.ylim(0, 420)
plt.xlim(0, 420)
graph.grid()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.draw()

x1dda, y1dda, x2dda, y2dda = map(int, input("Input x1, y1, x2, y2 for DDA\n").split())
x1b, y1b, x2b, y2b = map(int, input("Input x1, y1, x2, y2 for Bresenham\n").split())
x1kp, y1kp, x2kp, y2kp = map(int, input("Input x1, y1, x2, y2 for Castle-Pitway\n").split())
start_time = time.time()
dda_algorithm(graph, x1dda, y1dda, x2dda, y2dda, "red")
end_time = time.time()
time_dda = end_time - start_time

start_time = time.time()
bresenham_algorithm(graph, x1b, y1b, x2b, y2b, "green")
end_time = time.time()
time_bresenham = end_time - start_time

start_time = time.time()
castle_pitway_algorithm(graph, x1kp, y1kp, x2kp, y2kp, "blue")
end_time = time.time()
time_castle_pitway = end_time - start_time

print("DDA algorithm time, s:", time_dda)
print("Bresenham algorithm time, s:", time_bresenham)
print("Castle-Pitway algorithm time, s:", time_castle_pitway)

tk.mainloop()
