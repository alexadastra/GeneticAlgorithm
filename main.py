import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Parameter_Set import Ui_MainWindow as PrSt  # класс окна с определением параметров
from Arena_Set import Arena_desing as ArSt  # класс окна с сеттингом арены
from Design import Main_Design as Des  # класс окна с оболочкой арены
from Arena_of_Cell import Arena  # внутренние классы алгоритма

class App(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле
        super(App, self).__init__()
        self.ui = PrSt()
        self.ui.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.ui.setButton.clicked.connect(lambda: self.arena_set())

    def arena_set(self):
        design = App1(self)
        design.rename()
        self.close()
        design.exec()

class App1(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        super(App1, self).__init__()
        self.ui = ArSt(self.root.ui.x_atribute.value(), self.root.ui.y_atribute.value())
        self.ui.setupUi(self)
        self.ui.setButton.clicked.connect(lambda: self.arena_create())

    def rename(self):
        self.setWindowTitle('Arena_Set')

    def alert(self):
        alarm = QMessageBox()
        alarm.setIcon(QMessageBox.Information)
        alarm.setWindowTitle("!!!")
        alarm.setText("Something wrong!")
        alarm.exec()


    def arena_create(self):
        if (len(self.ui.walls) > (int(self.ui.square) - int(self.ui.bots_input.value())
                                  - int(self.ui.poison_input.value()) - int(self.ui.food_input.value()))):
            self.alert()
        else:
            window = App2(self, self.root)
            window.rename()
            window.setwalls()
            self.close()
            window.generating()
            window.exec()

class App2(QtWidgets.QDialog):
    def __init__(self, root, root_win):
        self.root_win = root_win
        self.root = root
        self.walls = root.ui.walls
        super(App2, self).__init__()
        self.ui = Des(self, self.root_win.ui.x_atribute.value(), self.root_win.ui.y_atribute.value(), self.walls)
        self.ui.setupUi(self)
        self.count_of_bot = int(self.root.ui.bots_input.value())
        self.end_count = self.count_of_bot // 2
        self.start_poison = int(self.root.ui.poison_input.value())
        self.start_food = int(self.root.ui.food_input.value())
        self.started = False
        self.timer = QtCore.QTimer(interval=150)
        self.ui.startButton.clicked.connect(lambda: self.arena.move())
        self.ui.skipButton.clicked.connect(lambda: self.generation_skip(self.ui.skip_number.value()))

    def rename(self):
        self.setWindowTitle('Arena')

    def setwalls(self):
        for i in range(self.ui.height):
            for j in range(self.ui.width):
                if [j, i] in self.ui.walls:
                    self.ui.ColorConfiguration(4, j, i, 0)

    def generating(self):
        self.arena = Arena(self.ui, self.ui.width, self.ui.height, self.count_of_bot,
                      self.start_poison, self.start_food, self.end_count)
        self.arena.generation_start()
        self.timer.timeout.connect(self.arena.move)  # привязка ф-ии move
        self.timer.stop()

    def arena_startpause(self):
        if not self.started:
            self.timer.start()
            self.started = True
        else:
            self.timer.stop()
            self.started = False

    def generation_skip(self, N):
        print(N)


app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window_start = App()  # Создаём объект класса ExampleApp
window_start.setWindowTitle('Parameter_Set')
window_start.show()  # Показываем окно
app.exec_()  # и запускаем приложение
