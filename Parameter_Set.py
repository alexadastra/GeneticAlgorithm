from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(200, 120)
        # задание виджета centralwidget, на котором поместим интерфейс
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # ползунок, перемещеием которого задаётся ширина арены (х - координата)
        self.x_atribute = QtWidgets.QSlider(self.centralwidget)  # инициализация
        self.x_atribute.setGeometry(QtCore.QRect(0, 21, 160, 20))  # задание размеров и метса расположения
        self.x_atribute.setRange(2, 16)  # диапазон значений
        self.x_atribute.setValue(8)  # начальное значение
        self.x_atribute.setOrientation(QtCore.Qt.Horizontal)  # горизонтальное положение ползунка
        # окошко со значением ползунка
        self.x_output = QtWidgets.QTextBrowser(self.centralwidget)  # инициализация
        self.x_output.setGeometry(QtCore.QRect(160, 0, 40, 40))  # задание размеров и метса расположения
        # начальное значение окошка приравниваем к начальному ползунка
        self.x_output.setText(str(self.x_atribute.value()))
        # привязка отображение текущего значения ползунка
        self.x_atribute.valueChanged.connect(lambda: self.x_output.setText(str(self.x_atribute.value())))

        # ползунок, перемещеием которого задаётся высота арены (у - координата)
        self.y_atribute = QtWidgets.QSlider(self.centralwidget)  # тут то же самое всё
        self.y_atribute.setGeometry(QtCore.QRect(0, 64, 160, 20))
        self.y_atribute.setRange(2, 16)
        self.y_atribute.setValue(8)
        self.y_atribute.setOrientation(QtCore.Qt.Horizontal)
        # окошко со значением ползунка
        self.y_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.y_output.setGeometry(QtCore.QRect(160, 43, 40, 40))
        self.y_output.setText(str(self.y_atribute.value()))
        self.y_atribute.valueChanged.connect(lambda: self.y_output.setText(str(self.y_atribute.value())))

        # подписи к ползункам
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 131, 20))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 43, 131, 20))

        # кнопка, нажатие на которую означает принятие настроек
        self.setButton = QtWidgets.QPushButton("Create arena", self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(0, 80, 200, 40))  # закрепление на нужном месте

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # функция нанесения надписей
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Arena width (x dimension)"))
        self.label_2.setText(_translate("MainWindow", "Arena height (y dimension)"))