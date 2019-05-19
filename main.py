import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from Parameter_Set import Ui_MainWindow as PrSt  # класс окна с определением параметров
from Arena_Set import Main_Design as ArSt  # класс окна с сеттингом арены
from Design import Main_Design as Des  # класс окна с оболочкой арены
from Arena_of_Cells import Cell, Arena  # внутренние классы алгоритма

class App(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле
        super(App, self).__init__()
        self.ui = PrSt()
        self.ui.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.ui.setButton.clicked.connect(lambda: self.arena_set())

    def arena_set(self):
        design = App1()
        design.rename()
        self.close()
        design.exec()

class App1(QtWidgets.QDialog):
    def __init__(self):
        super(App1, self).__init__()
        self.ui = ArSt(window.ui.x_atribute.value(), window.ui.y_atribute.value())
        self.ui.setupUi(self)
        self.ui.setButton.clicked.connect(lambda: self.arena_create())

    def rename(self):
        self.setWindowTitle('Arena_Set')

    def arena_create(self):
        arena = App2(self.ui.walls)
        arena.rename()
        arena.setwalls()
        self.close()
        print(self.ui.walls)
        arena.generating()
        arena.exec()

class App2(QtWidgets.QDialog):
    def __init__(self, walls):
        self.walls = walls
        super(App2, self).__init__()
        self.ui = Des(window.ui.x_atribute.value(), window.ui.y_atribute.value(), self.walls)
        self.ui.setupUi(self)

    def rename(self):
        self.setWindowTitle('Arena')

    def setwalls(self):
        for i in range(self.ui.height):
            for j in range(self.ui.width):
                if [j, i] in self.ui.walls:
                    self.ui.ColorConfiguration(4, j, i, 0)

    def generating(self):
        string = design.ui.bots_input.toPlainText()
        print(string)
        print(arena.ui.height)
        # self.ar = Arena(arena.ui.width, arena.ui.height, int(design.ui.bots_label.value()), int(design.ui.bots_label.value() // 2))


app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window = App()  # Создаём объект класса ExampleApp
window.setWindowTitle('Parameter_Set')
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение
