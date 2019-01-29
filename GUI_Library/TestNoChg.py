# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestNumberChanger.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 959)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(470, 30, 561, 661))
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setStyleSheet("QTableWidget#tableWidget{\n"
"background-color: rgb(255, 255, 222);\n"
"color: white;\n"
"background-image:url(:/newPrefix/images/yellow.jpg);\n"
"color: Black;\n"
"}\n"
"")
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setRowCount(24)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(101)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(27)
        self.tableWidget.verticalHeader().setDefaultSectionSize(29)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(30, 30, 200, 80))
        self.toolButton.setStyleSheet("QToolButton#toolButton{\n"
"    font: Bold 11pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/SelectButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: lightgray;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton:pressed{\n"
"    font: Bold 11pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/SelectButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: lightgray;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}")
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(250, 30, 200, 80))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.toolButton_2.setFont(font)
        self.toolButton_2.setStyleSheet("QToolButton#toolButton_2 {\n"
"    font: Bold 10pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/RunButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: gold;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_2:pressed {\n"
"border-image:url(:/newPrefix/images/RunButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: gold;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}")
        self.toolButton_2.setAutoRaise(False)
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QtCore.QRect(30, 130, 200, 80))
        self.toolButton_3.setStyleSheet("QToolButton#toolButton_3{\n"
"    font: Bold 11pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/LoadButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: Black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_3:pressed{\n"
"    font: Bold 11pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/LoadButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: Black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_5 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_5.setGeometry(QtCore.QRect(30, 340, 200, 80))
        self.toolButton_5.setStyleSheet("QToolButton#toolButton_5{\n"
"    font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/WriteButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: lightgray;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_5:pressed{\n"
"    font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/WriteButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: lightgray;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.toolButton_5.setIconSize(QtCore.QSize(32, 35))
        self.toolButton_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_5.setObjectName("toolButton_5")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 240, 431, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 290, 431, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.toolButton_6 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_6.setGeometry(QtCore.QRect(470, 820, 200, 80))
        self.toolButton_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_6.setStyleSheet("QToolButton#toolButton_6{\n"
"font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ResetButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_6:pressed{\n"
"font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ResetButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.toolButton_6.setIconSize(QtCore.QSize(35, 35))
        self.toolButton_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_6.setObjectName("toolButton_6")
        self.toolButton_7 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_7.setGeometry(QtCore.QRect(830, 820, 200, 80))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.toolButton_7.setFont(font)
        self.toolButton_7.setAutoFillBackground(False)
        self.toolButton_7.setStyleSheet("QToolButton#toolButton_7{\n"
"font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ExitButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: white;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_7:pressed{\n"
"font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ExitButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: white;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.toolButton_7.setIconSize(QtCore.QSize(34, 34))
        self.toolButton_7.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_7.setObjectName("toolButton_7")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(135, 585, 180, 5))
        self.progressBar.setMinimum(0)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.toolButton_Find = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_Find.setGeometry(QtCore.QRect(470, 720, 200, 80))
        self.toolButton_Find.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_Find.setStyleSheet("QToolButton#toolButton_Find{\n"
"    font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/FindButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: yellow;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#toolButton_Find:pressed{\n"
"    font: Bold 12pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/FindButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: yellow;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.toolButton_Find.setIconSize(QtCore.QSize(35, 35))
        self.toolButton_Find.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_Find.setObjectName("toolButton_Find")
        self.lineEdit_Find = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Find.setGeometry(QtCore.QRect(700, 750, 301, 20))
        self.lineEdit_Find.setObjectName("lineEdit_Find")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 220, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 270, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(135, 670, 180, 5))
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setObjectName("progressBar_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 608, 170, 44))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("QLabel#label_3{\n"
"    font: 75 14pt \"MS Shell Dlg 2\";\n"
"border-image:transparent;\n"
"background: none;\n"
"color: rgb(85, 85, 255);\n"
"background-position: left;\n"
"}")
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHow_To_Use_Tool = QtWidgets.QAction(MainWindow)
        self.actionHow_To_Use_Tool.setObjectName("actionHow_To_Use_Tool")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuHelp.addAction(self.actionHow_To_Use_Tool)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionExit)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "Select UNA"))
        self.toolButton_2.setText(_translate("MainWindow", "Run\n"
"BinToBinExtract\n"
" Tool"))
        self.toolButton_3.setText(_translate("MainWindow", "  Load CSV File"))
        self.toolButton_5.setText(_translate("MainWindow", "Generate\n"
" Test IDs"))
        self.lineEdit.setText(_translate("MainWindow", "UNA File Location"))
        self.lineEdit_2.setText(_translate("MainWindow", "CSV File Location"))
        self.toolButton_6.setText(_translate("MainWindow", "  Reset"))
        self.toolButton_7.setText(_translate("MainWindow", "Exit"))
        self.toolButton_Find.setText(_translate("MainWindow", "  Find"))
        self.label.setText(_translate("MainWindow", "UNA File"))
        self.label_2.setText(_translate("MainWindow", "CSV File"))
        self.label_3.setText(_translate("MainWindow", "          Status\n"
"          "))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionHow_To_Use_Tool.setText(_translate("MainWindow", "How To Use Tool"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

import TNC_UI_R10_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

