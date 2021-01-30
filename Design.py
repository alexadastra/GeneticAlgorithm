from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Main_Design():
    # перегрузка параметров ширины и длины арены в клетках, координат и стен
    def __init__(self, root, width, height, walls):
        self.root = root
        self.width = width
        self.height = height
        self.walls = walls
        self.square = self.width * self.height
        self.i = 0
        self.j = 0
        self.side = 40

    # описание основного дизайна
    def setupUi(self, Main_Window):
        # размеры окна
        Main_Window.setFixedSize(int(self.side) * int(self.width) + 256, int(self.side) * (int(self.height) + 2))
        # задание виджета centralwidget, на котором поместим основные штуковины
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        # инициализация клеток как массива квадратов с выводом текста (textbrowser)
        self.texts = [[QtWidgets.QTextBrowser(self.centralwidget) for j in range(self.width)] for i in
                      range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#808080}")  # стандартный цвет серый
                # self.central.addWidget(self.texts[i][j], i, j)  # вставка в нужное место сетки
                self.texts[i][j].setGeometry(QtCore.QRect(self.side * j, self.side * i, self.side, self.side))

        # кнопка по управлению симуляцией (вкл-выкл)
        self.startButton = QtWidgets.QPushButton("Start/Stop", self.centralwidget)  # инициализация
        self.startButton.setGeometry(QtCore.QRect(0, self.height * self.side,
                                                  self.width * self.side, self.side))  # закрепление на нужном месте

        # кнопка по пропуску поколений
        self.skipButton = QtWidgets.QPushButton("Skip n generations", self.centralwidget)  # инициализация
        self.skipButton.setGeometry(QtCore.QRect(0, (self.height + 1) * self.side,
                                                 self.width * self.side, self.side))  # закрепление на нужном месте

        #число пропуска поколений
        self.skip_number = QtWidgets.QSpinBox(self.centralwidget)
        self.skip_number.setGeometry(QtCore.QRect(self.width * self.side,
                                                  (self.height + 1) * self.side, 256, self.side))  # размеры
        self.skip_number.setRange(100, 10000)

        # вывод в окошко раличной информации(для дебага и отслежки работы)
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 30, 256,
                                             int(self.side) * int(self.height) + self.side - 30))  # размеры

        # ярлык для красоты
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 0, 256, 30))

        # служебные функции потому что надо
        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    #включение текста в виджеты
    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "    State:"))

    # основная функция взаимодействия с окном: изменение конфигураций клеток
    def ColorConfiguration(self, obj, j, i, hp):
        if obj != 1:  # если не бот
            if obj == 0:  # пустота
                self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#808080}")  # серый цвет
            elif obj == 2:  # еда
                self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#008000}")  # зелёный цвет
            elif obj == 3:  # яд
                self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#FF4500}")  # тёмно-оранжевый
            elif obj == 4:  # стена
                self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#000000}")  # чёрный
            self.texts[i][j].setText('')
        else:
            self.texts[i][j].setStyleSheet("QTextBrowser {background-color:#6A5ACD}")  # голубой
            self.texts[i][j].setText(str(hp))  # в тексте здоровье бота
