# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestNumberChanger_Rev2.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 1000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/TNC_Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(630, 20, 531, 711))
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
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(101)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(27)
        self.tableWidget.verticalHeader().setDefaultSectionSize(29)
        self.tableWidget.verticalHeader().setMinimumSectionSize(24)
        self.Bin2BinButton = QtWidgets.QToolButton(self.centralwidget)
        self.Bin2BinButton.setGeometry(QtCore.QRect(40, 30, 250, 80))
        self.Bin2BinButton.setMinimumSize(QtCore.QSize(250, 80))
        self.Bin2BinButton.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Bin2BinButton.setFont(font)
        self.Bin2BinButton.setStyleSheet("QToolButton#Bin2BinButton {\n"
"    font: Bold 13pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/RunButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: gold;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#Bin2BinButton:pressed {\n"
"border-image:url(:/newPrefix/images/RunButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: gold;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}")
        self.Bin2BinButton.setAutoRaise(False)
        self.Bin2BinButton.setObjectName("Bin2BinButton")
        self.LoadCSVButton = QtWidgets.QToolButton(self.centralwidget)
        self.LoadCSVButton.setGeometry(QtCore.QRect(320, 30, 250, 80))
        self.LoadCSVButton.setMinimumSize(QtCore.QSize(250, 80))
        self.LoadCSVButton.setMaximumSize(QtCore.QSize(250, 80))
        self.LoadCSVButton.setStyleSheet("QToolButton#LoadCSVButton{\n"
"    font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/LoadButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: Black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#LoadCSVButton:pressed{\n"
"    font: Bold 14pt \"Candara\";\n"
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
        self.LoadCSVButton.setObjectName("LoadCSVButton")
        self.GenTestIDButton = QtWidgets.QToolButton(self.centralwidget)
        self.GenTestIDButton.setGeometry(QtCore.QRect(40, 250, 250, 80))
        self.GenTestIDButton.setMinimumSize(QtCore.QSize(250, 80))
        self.GenTestIDButton.setMaximumSize(QtCore.QSize(250, 80))
        self.GenTestIDButton.setStyleSheet("QToolButton#GenTestIDButton{\n"
"    font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/WriteButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: lightgray;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#GenTestIDButton:pressed{\n"
"    font: Bold 14pt \"Candara\";\n"
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
        self.GenTestIDButton.setIconSize(QtCore.QSize(32, 35))
        self.GenTestIDButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.GenTestIDButton.setObjectName("GenTestIDButton")
        self.UNALineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.UNALineEdit.setGeometry(QtCore.QRect(50, 150, 441, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.UNALineEdit.setFont(font)
        self.UNALineEdit.setObjectName("UNALineEdit")
        self.CSVLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CSVLineEdit.setGeometry(QtCore.QRect(50, 200, 441, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.CSVLineEdit.setFont(font)
        self.CSVLineEdit.setObjectName("CSVLineEdit")
        self.ResetButton = QtWidgets.QToolButton(self.centralwidget)
        self.ResetButton.setGeometry(QtCore.QRect(620, 860, 250, 80))
        self.ResetButton.setMinimumSize(QtCore.QSize(250, 80))
        self.ResetButton.setMaximumSize(QtCore.QSize(250, 80))
        self.ResetButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ResetButton.setStyleSheet("QToolButton#ResetButton{\n"
"font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ResetButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: black;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#ResetButton:pressed{\n"
"font: Bold 14pt \"Candara\";\n"
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
        self.ResetButton.setIconSize(QtCore.QSize(35, 35))
        self.ResetButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.ResetButton.setObjectName("ResetButton")
        self.ExitButton = QtWidgets.QToolButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(910, 860, 250, 80))
        self.ExitButton.setMinimumSize(QtCore.QSize(250, 80))
        self.ExitButton.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ExitButton.setFont(font)
        self.ExitButton.setAutoFillBackground(False)
        self.ExitButton.setStyleSheet("QToolButton#ExitButton{\n"
"font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/ExitButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: white;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#ExitButton:pressed{\n"
"font: Bold 14pt \"Candara\";\n"
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
        self.ExitButton.setIconSize(QtCore.QSize(34, 34))
        self.ExitButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.ExitButton.setObjectName("ExitButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(135, 585, 180, 5))
        self.progressBar.setMinimum(0)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.FindButton = QtWidgets.QToolButton(self.centralwidget)
        self.FindButton.setGeometry(QtCore.QRect(620, 760, 250, 80))
        self.FindButton.setMinimumSize(QtCore.QSize(250, 80))
        self.FindButton.setMaximumSize(QtCore.QSize(250, 80))
        self.FindButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.FindButton.setStyleSheet("QToolButton#FindButton{\n"
"font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/FindButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: yellow;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#FindButton:pressed{\n"
"font: Bold 14pt \"Candara\";\n"
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
        self.FindButton.setIconSize(QtCore.QSize(35, 35))
        self.FindButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.FindButton.setObjectName("FindButton")
        self.FindLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.FindLineEdit.setGeometry(QtCore.QRect(890, 790, 261, 20))
        self.FindLineEdit.setStyleSheet("QLineEdit#FindLineEdit{\n"
"background-color: rgb(255, 255, 222);\n"
"color: Black;\n"
"}\n"
"")
        self.FindLineEdit.setObjectName("FindLineEdit")
        self.UNALabel = QtWidgets.QLabel(self.centralwidget)
        self.UNALabel.setGeometry(QtCore.QRect(50, 130, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.UNALabel.setFont(font)
        self.UNALabel.setObjectName("UNALabel")
        self.CSVLabel = QtWidgets.QLabel(self.centralwidget)
        self.CSVLabel.setGeometry(QtCore.QRect(50, 180, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSVLabel.setFont(font)
        self.CSVLabel.setObjectName("CSVLabel")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(135, 670, 180, 5))
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setObjectName("progressBar_2")
        self.StatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.StatusLabel.setGeometry(QtCore.QRect(120, 562, 211, 131))
        self.StatusLabel.setAutoFillBackground(False)
        self.StatusLabel.setStyleSheet("QLabel#StatusLabel{\n"
"    font: 75 14pt \"MS Shell Dlg 2\";\n"
"border-image:transparent;\n"
"background: none;\n"
"color: rgb(85, 85, 255);\n"
"background-position: left;\n"
"}")
        self.StatusLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.StatusLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.StatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StatusLabel.setObjectName("StatusLabel")
        self.FilesModLabel = QtWidgets.QLabel(self.centralwidget)
        self.FilesModLabel.setGeometry(QtCore.QRect(70, 380, 170, 21))
        self.FilesModLabel.setAutoFillBackground(False)
        self.FilesModLabel.setStyleSheet("QLabel#FilesModLabel{\n"
"    font: 75 14pt \"MS Shell Dlg 2\";\n"
"border-image:transparent;\n"
"background: none;\n"
"color: rgb(85, 85, 255);\n"
"background-position: left;\n"
"}")
        self.FilesModLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.FilesModLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.FilesModLabel.setObjectName("FilesModLabel")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(70, 400, 481, 81))
        self.listWidget.setObjectName("listWidget")
        self.SaveButton = QtWidgets.QToolButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(320, 250, 250, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveButton.sizePolicy().hasHeightForWidth())
        self.SaveButton.setSizePolicy(sizePolicy)
        self.SaveButton.setMinimumSize(QtCore.QSize(250, 80))
        self.SaveButton.setMaximumSize(QtCore.QSize(250, 80))
        self.SaveButton.setStyleSheet("QToolButton#SaveButton{\n"
"    font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/SaveButton1.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: yellow;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"QToolButton#SaveButton:pressed{\n"
"    font: Bold 14pt \"Candara\";\n"
"border-image:url(:/newPrefix/images/SaveButtonDn.png);\n"
"background: none;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;\n"
"color: yellow;\n"
"padding-left: 1px;\n"
"padding-right:70px;\n"
"}\n"
"")
        self.SaveButton.setIconSize(QtCore.QSize(32, 35))
        self.SaveButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.SaveButton.setObjectName("SaveButton")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 840, 111, 101))
        self.graphicsView.setStyleSheet("border-image:url(:/newPrefix/images/TNC_Icon.png);\n"
"background: transparent;\n"
"border: none;\n"
"background-color: transparent;\n"
"background-position: left;")
        self.graphicsView.setObjectName("graphicsView")
        self.KEYLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.KEYLineEdit.setGeometry(QtCore.QRect(510, 150, 71, 20))
        self.KEYLineEdit.setObjectName("KEYLineEdit")
        self.KEYLabel = QtWidgets.QLabel(self.centralwidget)
        self.KEYLabel.setGeometry(QtCore.QRect(510, 130, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.KEYLabel.setFont(font)
        self.KEYLabel.setObjectName("KEYLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet("QMenuBar#menubar{\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 85, 255);\n"
"}")
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.menuHelp.setFont(font)
        self.menuHelp.setStyleSheet("QMenu#menuHelp{ \n"
"color:rgb(85, 85, 255);\n"
"}\n"
"\n"
"")
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionHow_To_Use_Tool = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/images/TNC_Icon_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHow_To_Use_Tool.setIcon(icon1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.actionHow_To_Use_Tool.setFont(font)
        self.actionHow_To_Use_Tool.setObjectName("actionHow_To_Use_Tool")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/images/aboutIcon_small.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/images/door_exit_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.actionExit.setFont(font)
        self.actionExit.setObjectName("actionExit")
        self.menuHelp.addAction(self.actionHow_To_Use_Tool)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionExit)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Test Number Changer V1.2"))
        self.Bin2BinButton.setStatusTip(_translate("MainWindow", "Select una and BinToBinExtracter "))
        self.Bin2BinButton.setText(_translate("MainWindow", "Select UNA File \n"
" BinToBinExtract"))
        self.LoadCSVButton.setStatusTip(_translate("MainWindow", "Load a csv file"))
        self.LoadCSVButton.setText(_translate("MainWindow", "Load CSV File"))
        self.GenTestIDButton.setStatusTip(_translate("MainWindow", "Generate the TestID\'s"))
        self.GenTestIDButton.setText(_translate("MainWindow", "Generate\n"
" Test IDs"))
        self.UNALineEdit.setStatusTip(_translate("MainWindow", "una File Name"))
        self.UNALineEdit.setText(_translate("MainWindow", "UNA_File_Name"))
        self.CSVLineEdit.setStatusTip(_translate("MainWindow", "csv File Name"))
        self.CSVLineEdit.setText(_translate("MainWindow", "CSV_File_Name"))
        self.ResetButton.setStatusTip(_translate("MainWindow", "Reset Values"))
        self.ResetButton.setText(_translate("MainWindow", "  Reset"))
        self.ExitButton.setStatusTip(_translate("MainWindow", "Quit the program"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.FindButton.setStatusTip(_translate("MainWindow", "Find Test ID or TestName"))
        self.FindButton.setText(_translate("MainWindow", "  Find"))
        self.FindLineEdit.setStatusTip(_translate("MainWindow", "Search text"))
        self.UNALabel.setText(_translate("MainWindow", "UNA File"))
        self.CSVLabel.setText(_translate("MainWindow", "CSV File"))
        self.StatusLabel.setWhatsThis(_translate("MainWindow", "Status Message"))
        self.StatusLabel.setText(_translate("MainWindow", "Status"))
        self.FilesModLabel.setText(_translate("MainWindow", "Files Created"))
        self.listWidget.setStatusTip(_translate("MainWindow", "Files cretaed with TestID updates"))
        self.SaveButton.setStatusTip(_translate("MainWindow", "Save updated csv file."))
        self.SaveButton.setText(_translate("MainWindow", "Save CSV\n"
" Update"))
        self.KEYLineEdit.setToolTip(_translate("MainWindow", "Customization  Key"))
        self.KEYLabel.setText(_translate("MainWindow", "Key"))
        self.menuHelp.setStatusTip(_translate("MainWindow", "Main Menu"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionHow_To_Use_Tool.setText(_translate("MainWindow", "How To Use Tool"))
        self.actionHow_To_Use_Tool.setStatusTip(_translate("MainWindow", "Help Menu"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "About Program"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Quit Program"))

import TNC_UI_R10_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

