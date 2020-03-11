# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_lsb.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 553)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sourceText2 = QtWidgets.QTextEdit(self.centralwidget)
        self.sourceText2.setGeometry(QtCore.QRect(30, 20, 571, 31))
        self.sourceText2.setReadOnly(True)
        self.sourceText2.setObjectName("sourceText2")
        self.decodeText = QtWidgets.QTextEdit(self.centralwidget)
        self.decodeText.setGeometry(QtCore.QRect(110, 420, 421, 71))
        self.decodeText.setObjectName("decodeText")
        self.decodeButton = QtWidgets.QPushButton(self.centralwidget)
        self.decodeButton.setGeometry(QtCore.QRect(460, 390, 75, 23))
        self.decodeButton.setObjectName("decodeButton")
        self.encodeButton = QtWidgets.QPushButton(self.centralwidget)
        self.encodeButton.setGeometry(QtCore.QRect(110, 390, 75, 23))
        self.encodeButton.setObjectName("encodeButton")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(180, 90, 261, 261))
        self.image.setMaximumSize(QtCore.QSize(511, 511))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("Original_image/lenna.png"))
        self.image.setObjectName("image")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionUpload = QtWidgets.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.actionUpload.triggered.connect(self.openImage)
        self.toolBar.addAction(self.actionUpload)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openImage(self):
        self.imagePath, _ = QtWidgets.QFileDialog.getOpenFileName()
        print(self.imagePath)
        #self.pixmap = QtGui.QPixmap(self.imagePath)
        #self.image.setPixmap(self.pixmap)
        #self.resize(self.pixmap.size())
        #self.resize()
        #self.adjustSize()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.decodeButton.setText(_translate("MainWindow", "DECODE"))
        self.encodeButton.setText(_translate("MainWindow", "ENCODE"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionUpload.setText(_translate("MainWindow", "Upload"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
