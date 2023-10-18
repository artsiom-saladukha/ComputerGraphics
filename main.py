import colorsys
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

RGB_SCALE = 255
CMYK_SCALE = 100

root = tk.Tk()
root.title('Color Model Chooser')
root.geometry('480x240')


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def refresh_red(new_value):
    red.set(new_value)
    change_color()


def refresh_green(new_value):
    green.set(new_value)
    change_color()


def refresh_blue(new_value):
    blue.set(new_value)
    change_color()


def refresh_h(new_value):
    rgb = hls_to_rgb(float(new_value), float(lightness.get()), float(saturation.get()))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_l(new_value):
    rgb = hls_to_rgb(float(hue.get()), float(new_value), float(saturation.get()))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_s(new_value):
    rgb = hls_to_rgb(float(hue.get()), float(lightness.get()), float(new_value))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_c(new_value):
    rgb = cmyk_to_rgb(float(new_value), float(magenta.get()), float(yellow.get()), float(key.get()))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_m(new_value):
    rgb = cmyk_to_rgb(float(cyan.get()), float(new_value), float(yellow.get()), float(key.get()))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_y(new_value):
    rgb = cmyk_to_rgb(float(cyan.get()), float(magenta.get()), float(new_value), float(key.get()))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


def refresh_k(new_value):
    rgb = cmyk_to_rgb(float(cyan.get()), float(magenta.get()), float(yellow.get()), float(new_value))
    # red.set(rgb[0])
    # green.set(rgb[1])
    # blue.set(rgb[2])
    # change_color()


red, green, blue = (tk.Scale(root, from_=0, to=RGB_SCALE, orient='horizontal', command=refresh_red),
                    tk.Scale(root, from_=0, to=RGB_SCALE, orient='horizontal', command=refresh_green),
                    tk.Scale(root, from_=0, to=RGB_SCALE, orient='horizontal', command=refresh_blue))
red.grid(row=2, column=0, rowspan=1, columnspan=1)
green.grid(row=2, column=1, rowspan=1, columnspan=1)
blue.grid(row=2, column=2, rowspan=1, columnspan=1)
description = ttk.Label(root, text='RGB')
description.grid(row=2, column=3, rowspan=1, columnspan=1)

cyan, magenta, yellow, key = (tk.Scale(root, from_=0, to=CMYK_SCALE, orient='horizontal', command=refresh_c),
                              tk.Scale(root, from_=0, to=CMYK_SCALE, orient='horizontal', command=refresh_m),
                              tk.Scale(root, from_=0, to=CMYK_SCALE, orient='horizontal', command=refresh_y),
                              tk.Scale(root, from_=0, to=CMYK_SCALE, orient='horizontal', command=refresh_k))
cyan.grid(row=3, column=0, rowspan=1, columnspan=1)
magenta.grid(row=3, column=1, rowspan=1, columnspan=1)
yellow.grid(row=3, column=2, rowspan=1, columnspan=1)
key.grid(row=3, column=3, rowspan=1, columnspan=1)
description = ttk.Label(root, text='CMYK')
description.grid(row=3, column=4, rowspan=1, columnspan=1)

hue, lightness, saturation = (tk.Scale(root, from_=0, to=100, orient='horizontal', command=refresh_h),
                              tk.Scale(root, from_=0, to=100, orient='horizontal', command=refresh_l),
                              tk.Scale(root, from_=0, to=100, orient='horizontal', command=refresh_s))
hue.grid(row=4, column=0, rowspan=1, columnspan=1)
lightness.grid(row=4, column=1, rowspan=1, columnspan=1)
saturation.grid(row=4, column=2, rowspan=1, columnspan=1)
description = ttk.Label(root, text='HLS')
description.grid(row=4, column=3, rowspan=1, columnspan=1)


def cmyk_to_rgb(c, m, y, k):
    r = RGB_SCALE * (1.0 - c / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    g = RGB_SCALE * (1.0 - m / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    b = RGB_SCALE * (1.0 - y / float(CMYK_SCALE)) * (1.0 - k / float(CMYK_SCALE))
    return r, g, b


def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, CMYK_SCALE

    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    min_cmyk = min(c, m, y)

    c = (c - min_cmyk) / (1 - min_cmyk)
    m = (m - min_cmyk) / (1 - min_cmyk)
    y = (y - min_cmyk) / (1 - min_cmyk)
    k = min_cmyk

    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE


def rgb_to_hls(r, g, b):
    return colorsys.rgb_to_hls(r, g, b)


def hls_to_rgb(h, l, s):
    return colorsys.hls_to_rgb(h, l, s)


def cmyk_to_hls(c, m, y, k):
    return rgb_to_hls(cmyk_to_rgb(c, m, y, k)[0], cmyk_to_rgb(c, m, y, k)[1], cmyk_to_rgb(c, m, y, k)[2])


def hls_to_cmyk(h, l, s):
    return rgb_to_cmyk(hls_to_rgb(h, l, s)[0], hls_to_rgb(h, l, s)[1], hls_to_rgb(h, l, s)[2])


def ask_color():
    colors = askcolor(title="Tkinter Color Chooser")
    print(colors)
    label.configure(background=colors[1])
    red.set(colors[0][0])
    green.set(colors[0][1])
    blue.set(colors[0][2])

    cmyk = rgb_to_cmyk(colors[0][0], colors[0][1], colors[0][2])
    cyan.set(cmyk[0])
    magenta.set(cmyk[1])
    yellow.set(cmyk[2])
    key.set(cmyk[3])

    hls = rgb_to_hls(colors[0][0], colors[0][1], colors[0][2])
    hue.set(hls[0] * 100)
    lightness.set(hls[1] * 100)
    saturation.set(hls[2] * 100)


def change_color():
    hex_color = rgb_to_hex(red.get(), green.get(), blue.get())
    label.configure(background=hex_color)
    cmyk = rgb_to_cmyk(red.get(), green.get(), blue.get())
    cyan.set(cmyk[0])
    magenta.set(cmyk[1])
    yellow.set(cmyk[2])
    key.set(cmyk[3])

    hls = rgb_to_hls(red.get(), green.get(), blue.get())
    hue.set(hls[0] * 100)
    lightness.set(hls[1] * 100)
    saturation.set(hls[2] * 100)


label = ttk.Label(root, text='Current Color')
label.grid(row=0, column=1, rowspan=1, columnspan=1)
ttk.Button(
    root,
    text='Select a Color',
    command=ask_color).grid(row=1, column=1, rowspan=1, columnspan=1)
root.mainloop()
