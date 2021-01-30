import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from Parameter_Set import Ui_MainWindow as PrSt  # класс окна с определением параметров
from Arena_Set import Arena_desing as ArSt  # класс окна с сеттингом арены
from Design import Main_Design as Des  # класс окна с оболочкой арены
from Arena_of_Cell import Arena  # внутренние классы алгоритма


# при некорректно введённых данных всплывает окошко об ошибке
def alert():
    alarm = QMessageBox()
    alarm.setIcon(QMessageBox.Information)
    alarm.setWindowTitle("!!!")
    alarm.setText("Something wrong!")
    alarm.exec()


# класс первого окна с определением параметров
class App(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле
        super(App, self).__init__()
        self.ui = PrSt()  # подгрузка дизайна из модуля Parameter_Set
        self.ui.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.ui.setButton.clicked.connect(lambda: self.arena_set())  # при нажатии на кнопку

    # зовётся вот эта функция
    def arena_set(self):
        design = App1(self)  # инициализация объекта класса второго окна
        design.setWindowTitle('Arena_Set')  # переименовывание окна
        self.close()  # закрытие старого окна
        design.exec()  # и открытие нового


# класс окна с настройками арены и алгоритма
class App1(QtWidgets.QDialog):
    def __init__(self, root):
        self.root = root
        super(App1, self).__init__()
        # подгрузка дизайна из модуля Arena_Set, учитывая раннее указанные параметры
        self.ui = ArSt(self.root.ui.x_atribute.value(), self.root.ui.y_atribute.value())
        self.ui.setupUi(self)
        self.ui.setButton.clicked.connect(lambda: self.arena_create())

    # функция, привязанная к нажатию на основную кнопку
    def arena_create(self):
        # если какие-то параметры обозначены противоречиво или некорректно, заявляем об ошибке
        if (len(self.ui.walls) > (int(self.ui.square) - int(self.ui.bots_input.value())
                                  - int(self.ui.poison_input.value()) - int(self.ui.food_input.value()))) \
                or (self.ui.bots_input.value() < self.ui.mutation_input.value()):
            alert()
        else:  # если всё в порядке, то открываем новое окно
            window = App2(self, self.root)
            window.setWindowTitle('Arena')
            window.setwalls()
            self.close()
            window.generating()
            window.exec()


# класс основного окна(здесь происходит симуляция поколений и всё такое)
class App2(QtWidgets.QDialog):
    def __init__(self, root, root_win):
        # здесь перечислены все параметры, которые указывались в других окнах:
        self.root_win = root_win  # ссылка на объект App1
        self.root = root  # ссылка на объект App2
        self.walls = root.ui.walls  # массив стен
        super(App2, self).__init__()
        # подгрузка дизайна из модуля Design, учитывая длину-шириу арены и расположеие стен
        self.ui = Des(self, self.root_win.ui.x_atribute.value(), self.root_win.ui.y_atribute.value(), self.walls)
        self.ui.setupUi(self)
        self.count_of_bot = int(self.root.ui.bots_input.value())  # начальное количество ботов
        self.end_count = self.count_of_bot // 2  # количество ботов, на котором поколение обрвывается
        self.start_poison = int(self.root.ui.poison_input.value())  # начальное количество яда
        self.start_food = int(self.root.ui.food_input.value())  # яда
        self.number_mutation = int(self.root.ui.mutation_input.value())  # количество особей, которые мутируют
        self.genes_mutation = int(self.root.ui.genes_input.value())  # количество генов, которые будут изменены
        self.started = False  # указатель на начатость поколения
        self.timer = QtCore.QTimer(interval=125)  # таймер, регулирующий отображение симуляции
        self.ui.startButton.clicked.connect(lambda: self.arena_startpause())  # привязка функции паузы симуляции
        # привязка функции перемотки поколений на заданную величину
        self.ui.skipButton.clicked.connect(lambda: self.arena.move_skip(self.ui.skip_number.value()))

    # функция расставления стен по арене
    def setwalls(self):
        for i in range(self.ui.height):
            for j in range(self.ui.width):
                # если координаты клетки есть в массиве, то ставим там стену
                if [j, i] in self.ui.walls:
                    self.ui.ColorConfiguration(4, j, i, 0)

    # функция создания алгоритмической части арены
    def generating(self):
        # создание объекта класса Arena из модуля Arena_of_Cell
        self.arena = Arena(self, self.ui.width, self.ui.height, self.count_of_bot,
                           self.start_poison, self.start_food, self.end_count, self.genes_mutation,
                           self.number_mutation, self.walls)
        self.arena.generation_start()
        self.timer.timeout.connect(self.arena.move)  # привязка функции move к истечению таймера
        self.timer.stop()  # останавливаем таймер, чтобы он не делал глупостей

    # функция паузы/продолжения симуляции
    def arena_startpause(self):
        if not self.started:  # если поколение не начато
            self.timer.start()  # включаем таймер
            self.started = True  # даём сами себе знать об этом
            # отключаем кнопку перемотки, чтобы избежать случайных нажатий
            self.ui.skipButton.setEnabled(False)
        else:  # в противном случае - всё наоборот
            self.timer.stop()
            self.started = False
            self.ui.skipButton.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window_start = App()  # объект класса App
window_start.setWindowTitle('Parameter_Set')
window_start.show()  # Показываем окно
app.exec_()  # и запускаем приложение
