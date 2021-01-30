import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Arena_desing():
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
        Main_Window.setFixedSize(int(self.side) * int(self.width) + 256, int(self.side) * (int(self.height) + 1))
        # задание виджета centralwidget, на котором поместим интерфейс
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        # инициализация клеток как массива кнопок(при нажатии будут становиться стенами)
        self.texts = [[QtWidgets.QPushButton(self.centralwidget) for j in range(self.width)] for i in
                      range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                self.texts[i][j].setStyleSheet("QPushButton {background-color:#808080}")  # серый
                self.texts[i][j].setGeometry(QtCore.QRect(self.side * j, self.side * i, self.side, self.side))
                self.setfunc(i, j)  # к каждой клетке привяязываем функцию
        # подпись над переключалками
        self.sign = QtWidgets.QLabel(self.centralwidget)
        self.sign.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 0, 206, 20))
        # подпись к переключалке еды
        self.food_label = QtWidgets.QLabel(self.centralwidget)  # инициализация
        self.food_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 20, 206, 20))  # место и размеры
        # переключалка начального количества еды
        self.food_input = QtWidgets.QSpinBox(self.centralwidget)  # инициализация
        self.food_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 20, 50, 20))  # размеры
        self.food_input.setRange(1, self.square // 3)  # диапазон значений от 1 до трети площади арены
        self.food_input.setValue(self.square // 8)  # начальное значение

        # подпись к переключалке яда
        self.poison_label = QtWidgets.QLabel(self.centralwidget)
        self.poison_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 40, 206, 20))
        # переключалка начального количества яда
        self.poison_input = QtWidgets.QSpinBox(self.centralwidget)
        self.poison_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 40, 50, 20))
        self.poison_input.setRange(1, self.square // 3)
        self.poison_input.setValue(self.square // 8)

        # подпись к переключалке ботов
        self.bots_label = QtWidgets.QLabel(self.centralwidget)
        self.bots_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 60, 206, 20))
        # переключалка начального количества ботов
        self.bots_input = QtWidgets.QSpinBox(self.centralwidget)
        self.bots_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 60, 50, 20))  # размеры
        self.bots_input.setRange(1, self.square // 3)
        self.bots_input.setValue(self.square // 8)

        # подпись над переключалками
        self.sign2 = QtWidgets.QLabel(self.centralwidget)
        self.sign2.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 80, 206, 20))
        # подпись к переключалке мутирующих
        self.mutation_label = QtWidgets.QLabel(self.centralwidget)
        self.mutation_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 100, 206, 20))
        # переключалка количества мутирующих ботов
        self.mutation_input = QtWidgets.QSpinBox(self.centralwidget)
        self.mutation_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 100, 50, 20))  # размеры
        self.mutation_input.setRange(1, self.bots_input.value())
        self.mutation_input.setValue(2)

        # подпись к переключалке генов
        self.genes_label = QtWidgets.QLabel(self.centralwidget)
        self.genes_label.setGeometry(QtCore.QRect(int(self.side) * int(self.width), 120, 206, 20))
        # переключалка количества изменяющихся генов
        self.genes_input = QtWidgets.QSpinBox(self.centralwidget)
        self.genes_input.setGeometry(QtCore.QRect(int(self.side) * int(self.width) + 206, 120, 50, 20))  # размеры
        self.genes_input.setRange(0, 64)
        self.genes_input.setValue(1)

        # кнопка по генерации арены
        self.setButton = QtWidgets.QPushButton("Create arena", self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(0, self.height * self.side,
                                                self.width * self.side, self.side))  # закрепление на нужном месте

        # служебные функции потому что надо
        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    # включение текста в виджеты
    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        self.sign.setText(_translate("MainWindow", "Arena Settings:"))
        self.food_label.setText(_translate("MainWindow", str("  Basic food(from 1 to "
                                                             + str(self.square // 3) + "):")))
        self.poison_label.setText(_translate("MainWindow", str("  Basic poison (from 1 to "
                                                               + str(self.square // 3) + "):")))
        self.bots_label.setText(_translate("MainWindow", str("  Basic bots (from 1 to "
                                                             + str(self.square // 3) + "):")))
        self.sign2.setText(_translate("MainWindow", "Mutation Settings:"))
        self.mutation_label.setText(_translate("MainWindow", "  Bots changing(from 0 to 'Basic bots'): "))
        self.genes_label.setText(_translate("MainWindow", "  Genes changing(from 0 to 64): "))

    # функция по редактированию клетки при нажатии на неё
    def set_wall(self, x, y):
        if not([x, y] in self.walls):  # если клетки нет в массиве стен, добавляем её
            self.texts[y][x].setStyleSheet("QPushButton {background-color:#000000}")  # чёрный
            self.walls.append([x, y])
        else:  # если есть, то убираем
            self.texts[y][x].setStyleSheet("QPushButton {background-color:#808080}")  # серый
            self.walls.remove([x, y])

    def setfunc(self, a, b):
        self.texts[a][b].clicked.connect(lambda: self.set_wall(b, a))