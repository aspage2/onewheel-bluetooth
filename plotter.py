import time

import matplotlib.pyplot as plt

# Maps number of defined plots with a
plotnums = [
    110,
    110,
    120,
    130,
    220,
    230,
    230,
]


def plotter_main(recv_channel, plots):
    pts = {}
    running = True

    pn_base = plotnums[len(plots)]

    plt.ion()
    fig = plt.figure()

    for i, (uuid, plot_info) in enumerate(plots.items()):
        ax = fig.add_subplot(pn_base + i + 1)
        ax.set_title(plot_info.get("title", str(uuid)))
        pts[uuid] = {
            "xdata": [],
            "ydata": [],
            "line": ax.plot([], [])[0],
            "ax": ax,
        }

    first = last = time.time()

    while running:
        try:
            uuid, val = recv_channel()
        except OSError:
            print("pipe closed, stopping")
            running = False
        else:
            now = time.time()
            pt = pts[uuid]
            xdata = pt["xdata"]
            ydata = pt["ydata"]
            line = pt["line"]
            ax = pt["ax"]
            xdata.append(now - last)
            ydata.append(val)
            line.set_xdata(xdata)
            ax.set_xlim(-1, (now - first) * 1.1)
            line.set_ydata(ydata)
            ax.set_ylim(-10, max(ydata) * 1.1)
            fig.canvas.draw()
