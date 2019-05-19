import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Main_Design():
    # перегрузка параметров ширины и длины арены в клетках, координат и жы
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square = self.width * self.height
        self.walls = []
        self.i = 0
        self.j = 0
        self.side = 40

    # описание основного дизайна
    def setupUi(self, Main_Window):
        # размеры окна
        Main_Window.resize(int(self.side) * int(self.width) + 256, int(self.side) * (int(self.height) + 1))
        # задание виджета centralwidget, на котором поместим основные штуковины
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        # инициализация клеток как массива квадратов с выводом текста (textbrowser)
        self.texts = [[QtWidgets.QPushButton(self.centralwidget) for j in range(self.width)] for i in
                      range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                self.texts[i][j].setStyleSheet("QPushButton {background-color:#808080}")  # серый
                self.texts[i][j].setGeometry(QtCore.QRect(self.side * j, self.side * i, self.side, self.side))
                self.setfunc(i, j)

        self.food_label = QtWidgets.QLabel(self.centralwidget)
        self.food_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 0, 206, 20))
        self.food_intput = QtWidgets.QTextEdit(self.centralwidget)
        self.food_intput.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 0, 50, 20))  # размеры

        self.poison_label = QtWidgets.QLabel(self.centralwidget)
        self.poison_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 20, 256, 20))
        self.poison_intput = QtWidgets.QTextEdit(self.centralwidget)
        self.poison_intput.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 20, 50, 20))  # размеры

        self.bots_label = QtWidgets.QLabel(self.centralwidget)
        self.bots_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 40, 256, 20))
        self.bots_input = QtWidgets.QTextEdit(self.centralwidget)
        self.bots_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 40, 50, 20))  # размеры

        # кнопка по генерации арены
        self.setButton = QtWidgets.QPushButton("Create arena", self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(0, self.height * self.side,
                                                self.width * self.side, self.side))  # закрепление на нужном месте

        # служебные функции потому что надо
        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    #включение текста в виджеты
    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "Arena"))
        self.food_label.setText(_translate("MainWindow", str("Enter basic food amount(from 1 to "
                                                             + str(self.square // 3) + ":)")))
        self.poison_label.setText(_translate("MainWindow", str("Enter basic poison amount(from 1 to "
                                                               + str(self.square // 3) + ":)")))
        self.bots_label.setText(_translate("MainWindow", str("Enter basic bots amount(from 1 to "
                                                             + str(self.square // 3) + ":)")))

    def set_wall(self, x, y):
        if not([x, y] in self.walls):
            self.texts[y][x].setStyleSheet("QPushButton {background-color:#000000}")  # чёрный
            self.walls.append([x, y])
        else:
            self.texts[y][x].setStyleSheet("QPushButton {background-color:#808080}")  # серый
            self.walls.remove([x, y])

    def setfunc(self, a, b):
        self.texts[a][b].clicked.connect(lambda: self.set_wall(b, a))

