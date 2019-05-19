from PyQt5 import QtCore, QtGui, QtWidgets
import design

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 120)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.x_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.x_output.setGeometry(QtCore.QRect(160, 0, 40, 40))

        self.y_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.y_output.setGeometry(QtCore.QRect(160, 43, 40, 40))

        self.x_atribute = QtWidgets.QSlider(self.centralwidget)
        self.x_atribute.setGeometry(QtCore.QRect(0, 21, 160, 20))
        self.x_atribute.setMinimum(2)
        self.x_atribute.setMaximum(28)
        self.x_atribute.setOrientation(QtCore.Qt.Horizontal)
        self.x_atribute.valueChanged.connect(lambda: self.x_output.setText(str(self.x_atribute.value())))

        self.y_atribute = QtWidgets.QSlider(self.centralwidget)
        self.y_atribute.setGeometry(QtCore.QRect(0, 64, 160, 20))
        self.y_atribute.setMinimum(2)
        self.y_atribute.setMaximum(16)
        self.y_atribute.setOrientation(QtCore.Qt.Horizontal)
        self.y_atribute.valueChanged.connect(lambda: self.y_output.setText(str(self.y_atribute.value())))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 131, 20))

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 43, 131, 20))

        self.setButton = QtWidgets.QPushButton("Create arena", self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(0, 80, 200, 40))  # закрепление на нужном месте

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Arena width (x dimension)"))
        self.label_2.setText(_translate("MainWindow", "Arena height (y dimension)"))

