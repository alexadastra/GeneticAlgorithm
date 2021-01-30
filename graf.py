import matplotlib.pyplot as plot

def math_expr(args):
    data_x = []
    data_y = []
    for i in range(len(args)):
        data_x.append(i)
        data_y.append(args[i])

    plot.plot(data_x, data_y)
    plot.ylabel("Количество ходов")
    plot.plot(range(10), range(10))
    plot.savefig('graf.pdf')
