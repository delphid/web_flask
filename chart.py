import random

from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Page


def line_plot1(x, y, name='some data'):
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis(name, y)
    )
    return line

def bar_plot1(x, y, name='some data'):
    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis(name, y)
    )
    return bar

def line_plot(x, ys):
    line = Line().add_xaxis(x)
    for y_info in ys:
        line.add_yaxis(series_name=y_info[1], y_axis=y_info[0])
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    return line

def layout(*args):
    page = Page(layout=Page.SimplePageLayout)
    page.add(*args)
    page.render('render.html')


if __name__ == '__main__':
    y = [round(random.random() * 10, 2) for i in range(10)]
    x = [i for i in range(10)]
    line_plot(x, y)
