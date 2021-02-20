import random

from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Page


def line_plot(x, y):
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis('some data', y)
    )
    return line

def bar_plot(x, y):
    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis('some data', y)
    )
    return bar

def layout(*args):
    page = Page(layout=Page.SimplePageLayout)
    page.add(*args)
    page.render()


if __name__ == '__main__':
    y = [round(random.random() * 10, 2) for i in range(10)]
    x = [i for i in range(10)]
    line_plot(x, y)
