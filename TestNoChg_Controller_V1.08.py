from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import (Qt, pyqtSignal)
from GUI_Library.TestNoChg_V2 import *
import glob
import time,sys,datetime,re,os,pytest,subprocess,traceback
from subprocess import Popen, PIPE
from sys import exit
from collections import OrderedDict
#import pandas as pd
from GUI_Library.TNC_UI_R10_rc import *
from GUI_Library.MPP_Model_Misc302 import ParseFile
from collections import Counter
from threading import Timer
import glob
import shutil

if (sys.platform == "win32"):
    pdfCommand = ''
elif (sys.platform == "linux"):
    pdfCommand = 'acroread '
    pdfCommandDefault = 'evince '

Misc = ParseFile()
if (os.path.exists(Misc.resource_path("TNC_Help.pdf"))):
    tncHelpPath = Misc.resource_path("TNC_Help.pdf")
else:
    if(sys.platform == "win32"):
        tncHelpPath = '.\\Documents\\TNC_Help.pdf'
    elif(sys.platform == "linux"):
        tncHelpPath = './Documents/TNC_Help.pdf'

                
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class TNCToolWindow(QtWidgets.QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.uiVar = Ui_MainWindow()
        self.uiVar.setupUi(self)
        self.uiVar.Bin2BinButton.clicked.connect(self.Bin2Bin_ThreadRunner)
        self.uiVar.LoadCSVButton.clicked.connect(self.CSVFileSelect)
        self.uiVar.GenTestIDButton.clicked.connect(self.GenID_ThreadRunner)
        #self.uiVar.GenTestIDButton.hide()
        self.uiVar.SaveButton.clicked.connect(self.writeTabelToFile)
        #self.uiVar.SaveButton.hide()
        self.uiVar.ResetButton.clicked.connect(self.clearEntry)
        self.uiVar.ExitButton.clicked.connect(self.quit_prog)
        self.uiVar.FindButton.clicked.connect(self.findItem)
        self.uiVar.actionAbout.triggered.connect(self.about)
        self.uiVar.actionExit.triggered.connect(self.quit_prog)
        self.uiVar.actionHow_To_Use_Tool.triggered.connect(self.How_To_Use_TNC)
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar_2.hide()
        self.uiVar.FindLineEdit.setText('Search')
        self.uiVar.listWidget.hide()
        self.uiVar.FilesModLabel.hide()
        bg = "QLineEdit {background-color:rgb(255, 255, 191)}"
        self.uiVar.KEYLineEdit.setStyleSheet( bg )
        self.custKEY = ''

        self.csvDict={}
        self.headerColor()
        self.totalRows = 0
        self.mainDF=''
        self.updateDF=''
        self.tnFiles = []
        self.cwdDirs = []
        self.testNoUpdateDict = {}
        self.testDict = {}
        self.dupNoList = []
        
        self.fileCngCntDict = {}
        self.timeStamp = ''
        self.noUpdate = True
        self.dataClear = True
        self.csvDataList =[]
        self.csvDataListInit=[]
        self.csvLoad=False
        self.findRow=0
        self.findCol=0
        self.findString=''
        self.FileCanel = True
        self.ProgramVersion = ' V1.2 '
        self.CurrentReleaseDate = ' 01-18-2019 '
        self.showConsoleCommand = True
        self.process = ''
        self.Bin2BinComplete=False
        self.basePath = ''
        
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.threadpool = QThreadPool()
        self.progressValue = 0
        self.csvFilename = ''
        self.modifyList = ''
        self.loadCsvFlag = False
        self.changeCount = 0
        return
            
    def quit_prog(self):
        msgBox = QMessageBox(QMessageBox.Critical, ' ', 'Quit the program? ')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
        msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.png'))
        msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/door_exit_small.png'))
        ret = msgBox.exec_()
        if ret == QMessageBox.No:
            return
        #text="Exitting"
        #seq = "\x1b[1;%dm" % (30+4) + text + "\x1b[0m"
        #sys.stdout.write(seq)
        if (sys.platform == "linux"):
            self.cleanUpTmpDir()
        self.close()
        return

    def cleanUpTmpDir(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('.tmp_script1')))
        self.basePath = base_path
        sub_folders_pathname = '/tmp/_MEI*/'
        sub_folders_list = glob.glob(sub_folders_pathname)
        currentTmpDir = self.basePath+'/'
        if(currentTmpDir) in sub_folders_list:
            try:
                sub_folders_list.remove(currentTmpDir)
            except:
                pass
        for sub_folder in sub_folders_list:
            try:
                shutil.rmtree(sub_folder)
            except:
                pass
        return

    def env_var(self):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('Environment Variable QT_XKB_CONFIG_ROOT Required')
        box.setText('Please set environment variable QT_XKB_CONFIG_ROOT before using.\n\
 For csh/tsch shell enter:  setenv QT_XKB_CONFIG_ROOT /usr/share/X11/xkb\n \
 For bash shell enter:  export QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb\n\
Program will now close.')
        box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        box.setDefaultButton(QtWidgets.QMessageBox.Ok)
        box.setIcon(QtWidgets.QMessageBox.Critical)
        box.exec()
        return 

    def about(self):
        msgBox = QMessageBox(QMessageBox.Information, ' ',
        '<H2>About</H2> <H1>Test Number Changer</H1>\
        <br/><b> Created by T Arnold</b>\
        \n Dec 1, 2018<br/>Version '+self.ProgramVersion+self.CurrentReleaseDate)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
        msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.png'))
        msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/aboutIcon_small.png'))
        ret = msgBox.exec_()
        return

    def How_To_Use_TNC(self):
        if (os.path.exists(tncHelpPath)):
            if (os.path.exists("/usr/bin/evince")):
                p = subprocess.Popen(pdfCommandDefault+tncHelpPath, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell = True)
            else:
                p = subprocess.Popen(pdfCommand+tncHelpPath, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell = True)
        else:
            QMessageBox.warning(self,
            "Error",
            "Test Number Changer help file not found.\nCheck in original program Documents directory.")
        return
    
    def cellCheck(self):
        message=''
        count=0
        errorFlag=False
        self.noUpdate =False

        data = self.uiVar.tableWidget.item(1,0)
        if ((data is None) or (data.text() == '')):
            self.noUpdate = True
        if(self.noUpdate):
            if('GenID' in self.process):
                self.dialogMessageBoxWarning('No TestID Update Data to Generate?!')
            if('SaveCSV' in self.process):
                self.dialogMessageBoxWarning('No Table Data to Save?!')
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
            self.uiVar.StatusLabel.setText('Status')
            errorFlag=True
            return errorFlag

        for index in range(self.totalRows):
            data = self.uiVar.tableWidget.item(index,2)
            if (data is None):
                continue
            intFinder1 = re.compile('^(\d+)$')
            findINT = re.search(intFinder1,data.text())
            wordFinder1 = re.compile('^(\w+)$')
            findWRD = re.search(wordFinder1,data.text())
            if((findWRD) and not(findINT)) :
                self.uiVar.tableWidget.item(index, 2).setForeground(QtGui.QColor(234,0,0))
                errorFlag=True
                if(count ==0):
                    messageDialog="Please enter valid value(s) for cell("+str(index+1)+',3) '+data.text()+'\n'
                else:
                    messageDialog=messageDialog+"cell("+str(index+1)+',3) '+data.text()+'\n'
                count=count+1

        if(errorFlag):self.dialogMessageBoxError(messageDialog)
        return errorFlag
        
    def findItem(self):
        foundMatch = False
        searchText = self.uiVar.FindLineEdit.text()
        if not(searchText):
           searchText='Empty Field'
        for column in range(0,2):
            #print(column)
            if(column == 0):
                offset = 1
                Flag = True
            if(column == 1):
                offset = -1
                Flag = False
            Flag = False
            tempvar = 0
            self.model = self.uiVar.tableWidget.model()
            if not(self.findString==searchText.strip()):
                searchText = self.uiVar.FindLineEdit.text()
                self.findRow=0
            searchText = searchText.strip()  
            self.findString=searchText
            start = self.model.index(self.findRow, column)
            matches = self.model.match(
            start, QtCore.Qt.DisplayRole,
            searchText, -1, QtCore.Qt.MatchRecursive|QtCore.Qt.MatchStartsWith)
            #searchText, 1, QtCore.Qt.MatchStartsWith)

            if matches:
                foundMatch = True
                index = matches[0]
                self.uiVar.tableWidget.selectionModel().select(index, QItemSelectionModel.Select)
                self.uiVar.tableWidget.setCurrentCell(index.row(), index.column(),QItemSelectionModel.Current)
                self.uiVar.tableWidget.item(index.row(), index.column()).setBackground(QtGui.QColor(34,177,76))
                valueOffset = (0 if column else 1)
                valueOffset2 = (1 if column else 0)
                self.uiVar.tableWidget.item(index.row(), valueOffset).setBackground(QtGui.QColor(34,177,76))
                self.uiVar.tableWidget.item(index.row(), valueOffset2).setForeground(QtGui.QColor(234,0,0))
                self.findRow = index.row()+1
                self.findString=searchText.strip()
                if(self.findRow == self.totalRows):
                    self.findRow = 0
                    
        if not(foundMatch):
            if (self.findRow == 0):
                msgBox = QMessageBox(QMessageBox.Information, ' ',
                '<H2>Warning</H2> <H1>Cannot find: </H1> <H1>'+searchText+' </H1>')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
                msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.ico'))
                msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/TNC_Icon_small.png'))
                ret = msgBox.exec_()
                self.findRow = 0
            else:
                msgBox = QMessageBox(QMessageBox.Information, ' ',
                '<H2>Warning</H2> <H1>No other ocurrences for: </H1> <H1>'+searchText+' </H1>')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
                msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.ico'))
                msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/TNC_Icon_small.png'))
                ret = msgBox.exec_()
                self.findRow = 0
        return 

    def killProcess(self,p):
        try:
            self.Bin2BinComplete=True
            os.system("pkill "+p)
        except OSError:
            pass # ignore


    def UNAFileSelect(self):
        debugPrint = False
        self.FileCanel = False
        dlg2 = QtWidgets.QFileDialog()
        filter = 'UNA File (*.una)'
        if(debugPrint):print("Filter: "+filter)
        path= os.getcwd()
        filename =  dlg2.getOpenFileName(self, ' Select .una File',path,filter)
        configFile = str(filename)
        configFile = configFile.replace("('","")
        configFile = configFile.replace("', 'UNA File (*.una)')","")
        if(configFile == "', '')"):
            self.FileCanel = True
            return self.FileCanel
        self.uiVar.UNALineEdit.clear()
        self.uiVar.UNALineEdit.setText(configFile)
        bg = "QLineEdit {background-color:rgb(139, 233, 167)}"
        self.uiVar.UNALineEdit.setStyleSheet( bg )
        result = self.unaFileCheck(configFile)
        if not(result):
            self.dialogMessageBoxWarning('Not a una File!\n Unison:SyntaxRevision Header not found.')
            self.uiVar.UNALineEdit.setText('Wrong File Type/Contents.')
        return result

    def CSVFileSelect(self):
        result = self.checkAccessPrevilages()
        if(result):
            return
        debugPrint = False
        self.csvLoad=True
        self.FileCanel = False
        dlg2 = QtWidgets.QFileDialog()
        self.custKEY = self.uiVar.KEYLineEdit.text()
        filter = 'CSV File (*.csv)'
        if(debugPrint):print("Filter: "+filter)
        path= os.getcwd()
        writePrevilage = os.access(path, os.W_OK) # Check for write access
        if not(writePrevilage):
            messageDialog = "No write privilages for directory "+path+"!"
            self.dialogMessageBoxError(messageDialog)
            return
        filename =  dlg2.getOpenFileName(self, ' Select .csv File',path,filter)
        csvFile = str(filename)
        csvFile = csvFile.replace("('","")
        csvFile = csvFile.replace("', 'CSV File (*.csv)')","")
        if(csvFile == "', '')"):
            self.FileCanel = True
            return self.FileCanel
        self.uiVar.CSVLineEdit.clear()
        self.uiVar.CSVLineEdit.setText(csvFile)
        try:
            result = self.csvFileCheck(csvFile)
            if(result):
                self.readCVSToTable(csvFile)
                self.uiVar.GenTestIDButton.show()
                self.uiVar.SaveButton.show()
                self.loadCsvFlag = True
            if not(result):
                self.dialogMessageBoxWarning('Not a BinToBin CVS File!\nHeader not found.')
                self.uiVar.CSVLineEdit.setText('Wrong File Type/Contents.')
                self.uiVar.StatusLabel.setText( "CSV File Type Issue")
                self.loadCsvFlag = False
        except:
            pass
        return


    def dialogMessageBoxWarning(self,message):
            msgBox = QMessageBox(QMessageBox.Information, ' ',
            '<H2>Warning</H2> <H1> '+message +' </H1> ')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
            msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.ico'))
            msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/uncheckedcircle_small.png'))
            ret = msgBox.exec_()
            return

    def dialogMessageBoxError(self,message):
            msgBox = QMessageBox(QMessageBox.Critical, ' ',
            '<H1>Error</H1> <H2> '+message +' </H2> ')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
            msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.ico'))
            msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/uncheckedcircle_small.png'))
            ret = msgBox.exec_()
            return

        

    def headerColor(self):
        item1 = QtWidgets.QTableWidgetItem('Test Name')
        item1.setBackground(QtGui.QColor(255, 0, 0))
        self.uiVar.tableWidget.setHorizontalHeaderItem(0,item1)
        self.uiVar.tableWidget.setColumnWidth(0, 270)
        #self.uiVar.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        stylesheet = "::section{Background-color:rgb(145,192,240);border-radius:100px;}"
        self.uiVar.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        self.uiVar.tableWidget.verticalHeader().resizeSection(0, 45)
        header = self.uiVar.tableWidget.horizontalHeader() 
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        afont = QtGui.QFont()
        afont.setFamily("Arial Black")
        afont.setPointSize(18)
        self.uiVar.tableWidget.horizontalHeader().setFont(afont)


        item2 = QtWidgets.QTableWidgetItem('TestID')
        item2.setBackground(QtGui.QColor(0, 255, 0))
        self.uiVar.tableWidget.setHorizontalHeaderItem(1,item2)
        self.uiVar.tableWidget.setColumnWidth(1, 100)
        #self.uiVar.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        item3 = QtWidgets.QTableWidgetItem('TestID Update')
        item3.setBackground(QtGui.QColor(0, 0, 255))
        self.uiVar.tableWidget.setHorizontalHeaderItem(2,item3)
        self.uiVar.tableWidget.setColumnWidth(2, 110)
        #self.uiVar.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        return

    def ChangeSelectionColor(self):
        try:
            for item in self.uiVar.tableWidget.selectedItems():
                col=item.column()
            self.uiVar.tableWidget.setStyleSheet("QTableWidget::item:selected{ background-color: %s }"%color_list[col])
        except:
            pass
        #self.uiVar.tableWidget.setStyleSheet("background-color:#FDFEDA; color:YELLOW")
        return
    
    def columnColor(self,data,df,column):
        #for i in range(len(df.index)):
        item1 = QtWidgets.QTableWidgetItem(str(data))
        if(column == 0):
            item1.setBackground(QtGui.QColor(255, 0, 0))
        if(column == 1):
            item1.setBackground(QtGui.QColor(0, 255, 0))
        if(column == 2):
            item1.setBackground(QtGui.QColor(0, 0, 255))
        if(column == 3):
            item1.setBackground(QtGui.QColor(255, 0, 255))
        #self.uiVar.tableWidget.item(4,2).setBackgroundColor(QtGui.QColor(255, 0, 0))
        item4 = QtWidgets.QTableWidgetItem('Status')
        item4.setBackground(QtGui.QColor(0, 255, 255))
        #self.uiVar.tableWidget.setCurrentItem(item4)
        return

    def readCSVFile(self,csvfile):
        debgPrint = false
        fr = open(csvfile, "r",buffering=2)
        csvData = fr.readlines()
        fr.close()
        for line in csvData:
            if(("pere" in self.custKEY) and (len(self.custKEY) == 4) and (len(dataList) == 13 )):
                csvFinder1 = re.compile('^(\d+),([\w]+),([\w]+)?,([\w]+)?,([\w]+)?,([\w]+)?,([\w.]+)?,([\w.]+)?,([\w.]+)?,([\w.]+)?,([\w.]+)?,([\w.]+)?,([\w.]+)?')
                TNameGrpNo = 2
                TIdGrpNo = 1
                findCSV = re.search(csvFinder1,line)
                if(findCSV.group(2)):
                    TestName = sfindCSV.group(TNameGrpNo)
                    TestID = findCSV.group(TIdGrpNo)
            else:
                csvFinder1 = re.compile('^(\w+)\s*,([\w\s]+)\s*,([\w\s]+)\s*,?([\w\s]+)?\s*,?([\w\s]+)?\s*,?([\w\s]+)?\s*,?([\w\s]+)?\s*,?([\w\s]+)?')
                TNameGrpNo = 3
                TIdGrpNo = 2
                findCSV = re.search(csvFinder1,line)
                if(findCSV.group(3)):
                    TestName = sfindCSV.group(TNameGrpNo)
                    TestID = findCSV.group(TIdGrpNo)
            self.csvDict.update({TestName:TestID})
        if(debugPrint):print(self.csvDict)
        return
    
    def readCSVPandaToTable(self,csvfile):
        df = pd.read_csv(csvfile)
        self.uiVar.tableWidget.setColumnCount(4)
        self.uiVar.tableWidget.setRowCount(len(df.index))
        self.totalRows = len(df.index)
        for i in range(len(df.index)):
            for j in range(2):
                if((j==1) or (j==2)):
                    if(j==1):col = 2
                    if(j==2):col = 1
                    self.uiVar.tableWidget.setItem(i,j-1,QTableWidgetItem(str(df.iloc[i, col])))
                    item = QTableWidgetItem(str(df.iloc[i, col]))
                    item.setFlags(  QtCore.Qt.ItemIsEnabled )
                    self.uiVar.tableWidget.setItem(i,j-1, item)
                    #print(str(df.iloc[i, col]))
                    #print(j-1)
                    #self.columnColor(str(df.iloc[i, col]),df,j-1)
        self.mainDF = df
        self.backgroundTable()
        #self.writePandaToFile(mainDF,'Tyron Arnold.csv')
        return 

    def readCVSToTable(self,csvfile):
        csvDataList=[]
        dataList=[]
        counter=0
        self.csvDataList=[]
        self.csvDataListInit=[]
        dataOffset=0
        
        fr = open(csvfile, "r",buffering=1)
        csvData = fr.readlines()
        fr.close()
        for line in csvData:
            line = line.replace("\"", "")
            #print("R1")
            if(',,,LimitStructData,,,LocalLimits,,,,,,' in line):
                continue
            if(len(line) > 10):
                #print("R2")
                dataList = line.split(',')
                if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                    self.csvDataList.append([dataList[0],dataList[1],dataList[2],dataList[3],dataList[4],dataList[5],dataList[6],dataList[7],\
                    dataList[8],dataList[9],dataList[10],dataList[11],dataList[12]])
                    self.csvDataListInit.append([dataList[0],dataList[1],dataList[2],dataList[3],dataList[4],dataList[5],dataList[6],dataList[7],\
                    dataList[8],dataList[9],dataList[10],dataList[11],dataList[12]])
                    self.totalRows = counter
                    counter = counter+1
                else:
                    #print("R3")
                    self.csvDataList.append([dataList[0],dataList[1],dataList[2],dataList[3],dataList[4],dataList[5],dataList[6],dataList[7]])
                    self.csvDataListInit.append([dataList[0],dataList[1],dataList[2],dataList[3],dataList[4],dataList[5],dataList[6],dataList[7]])
                    self.totalRows = counter
                    counter = counter+1
        self.uiVar.tableWidget.clear()
        self.headerColor()
        self.uiVar.tableWidget.setColumnCount(3)
        self.uiVar.tableWidget.setRowCount(self.totalRows+1)
        totalRows=self.totalRows
        for i in range(totalRows+1):
            for j in range(3):
                if((j==1) or (j==2)):
                    if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                        if(j==1):col = 1
                        if(j==2):col = 0
                    else:
                        if(j==1):col = 2
                        if(j==2):col = 1
                    self.uiVar.tableWidget.setItem(i,j-1,QTableWidgetItem(str(self.csvDataList[i][col])))
                    item = QTableWidgetItem(str(self.csvDataList[i][col]))
                    item.setFlags(  QtCore.Qt.ItemIsEnabled )
                    self.uiVar.tableWidget.setItem(i,j-1, item)
        bg = "QLineEdit {background-color:rgb(139, 233, 167)}"
        self.uiVar.CSVLineEdit.setStyleSheet( bg )
        if(self.csvLoad):
            bg = "QLineEdit {background-color:rgb(251, 221, 151)}"
            self.uiVar.CSVLineEdit.setStyleSheet( bg )
        
    def writePandaToFile(self):
        self.updateDF = self.mainDF.copy()
        for index in range(self.totalRows):
            #progress_callback.emit(n)
            #n=n+1
            try:
                data = self.uiVar.tableWidget.item(index,2)
                if(data.text()):
                    self.noUpdate = False
                    ##print(data.text())
                    self.updateDF.at[index, 'Test Number'] = data.text()
            except:
                pass
        self.updateDF[['SW Bin', 'HW Bin']] = self.updateDF[['SW Bin', 'HW Bin']].astype(float64)
        #self.updateDF[ 'HW Bin'].astype(str).astype(int)

        print(self.updateDF.dtypes)
        csvFileToWrite = self.uiVar.CSVLineEdit.text()+'_mod'
        self.updateDF.to_csv(csvFileToWrite, sep=',', encoding='utf-8',index=False)
        return

    def writeTabelToFile(self):
        msgBox = QMessageBox(QMessageBox.Critical, ' ', 'Save CSV Table Now? ')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
        msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.png'))
        msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/saveDisk_small.png'))
        ret = msgBox.exec_()
        if ret == QMessageBox.No:
            return
        self.process = 'SaveCSV'
        status = self.cellCheck()
        if(status):
            return
        indexOffset=0
        for index in range(self.totalRows):
            #progress_callback.emit(n)
            #n=n+1
            if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                indexOffset=0
            try:
                self.csvDataList[index][1]=self.csvDataListInit[index][1]
                data = self.uiVar.tableWidget.item(index,2)
                if(data.text()):
                    self.noUpdate = False
                    ##print(data.text())
                    
                    if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                        self.csvDataList[index][0] = data.text()
                    else:
                        self.csvDataList[index][1] = data.text()
            except:
                pass
        ##############################################################################
        ##                      Duplicte TestId Code (May need one day)
        ##############################################################################
##        for i in range(self.totalRows+1):
##            TestName = self.csvDataList[i][2]
##            TestID = self.csvDataList[i][1]
##            self.testDict.update({TestName:TestID})
##            self.dupNoList.append(TestID)
##            
##        #print(self.dupNoList)
##        dupCountDict = Counter(self.dupNoList)
##        localDupList=[]
##        #print(dupCountDict)
##        
##        yourDuped = False
##        for key,val in dupCountDict.items():
##            if (val >1):
##                yourDuped = True
##                localDupList.append(str(key))
##        messageStr = 'Found duplicate Test Ids:\n'
##        for key,value in self.testDict.items():
##            if(value in localDupList):
##                messageStr = messageStr+str(value)+':'+str(key)+'\n'
##        if(yourDuped):
##            print(messageStr)
        #############################################################################
            
        csvFileToWrite = self.uiVar.CSVLineEdit.text()+'_mod'
##        writePrevilage = os.access(csvFileToWrite, os.W_OK) # Check for write access
##        if not(writePrevilage):
##            messageDialog = "No write privilages for "+csvFileToWrite+"!"
##            self.dialogMessageBoxError(messageDialog)
##            return
        fo = open(csvFileToWrite, "w",buffering=2)
        if (os.path.exists(csvFileToWrite)):
            doNothing = 1
            for i in range(self.totalRows+1):
                if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                    if(i == 0):
                        fo.write(',,,LimitStructData,,,LocalLimits,,,,,,\n')
                    fo.write(self.csvDataList[i][0]+','+self.csvDataList[i][1]+','+self.csvDataList[i][2]+','+self.csvDataList[i][3]+','+self.csvDataList[i][4]+','+self.csvDataList[i][5]+\
                    ','+self.csvDataList[i][6]+','+self.csvDataList[i][7]+','+self.csvDataList[i][8]+','+self.csvDataList[i][9]+','+self.csvDataList[i][10]+','+self.csvDataList[i][11]+','+self.csvDataList[i][12])
                else:
                    fo.write(self.csvDataList[i][0]+','+self.csvDataList[i][1]+','+self.csvDataList[i][2]+','+self.csvDataList[i][3]+','+self.csvDataList[i][4]+','+self.csvDataList[i][5]+\
                    ','+self.csvDataList[i][6]+','+self.csvDataList[i][7])
        fo.close()
        return


    def readTableDataPanda(self,progress_callback):
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar_2.hide()
        self.uiVar.StatusLabel.setText('Status')
        if(len(self.mainDF) == 0):
            return
        n=0
        self.mainDF['Test Number Update'] = '' 
        self.noUpdate = True
        for index in range(self.totalRows):
            progress_callback.emit(n)
            n=n+1
            try:
                data = self.uiVar.tableWidget.item(index,2)
                if(data.text()):
                    self.noUpdate = False
                ##print(data.text())
                self.mainDF.at[index, 'Test Number Update'] = data.text()
            except:
                pass
        #self.writePandaToFile('Tyron.csv')
        #print(self.mainDF.head())
        return

    def readTableData(self,progress_callback):
        n=0
        self.noUpdate = True
        for index in range(self.totalRows+1):
            progress_callback.emit(n)
            n=n+1
            try:
                if not(self.loadCsvFlag):
                    colNum = 2
                else:
                    colNum = 1
                data = self.uiVar.tableWidget.item(index,colNum)
                #print(data.text())
                if(data.text()):
                    self.noUpdate = False
                if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                    self.csvDataList[index][0] = data.text()
                else:
                    self.csvDataList[index][1] = data.text()
            except:
                pass
        return

    def updateTableData(self,progress_callback):
        self.modifyList = ''
        row=0
        n=0
        self.uiVar.Bin2BinButton.setEnabled(False)
        self.uiVar.GenTestIDButton.setEnabled(False)
        self.testNoUpdateDict = {}
        
        self.readTableData(progress_callback)
        if(self.noUpdate):
            return
        progress_callback.emit(n)
        n=n+1
        self.uiVar.listWidget.clear()
        self.testNoUpdateDict = {}
        for index in range(self.totalRows+1):
            progress_callback.emit(n)
            n=n+1
            if not(self.loadCsvFlag):
                colNum = 2
            else:
                colNum = 1

            data2 = self.uiVar.tableWidget.item(index,2)
            data = self.uiVar.tableWidget.item(index,colNum)
            if ((not(data2 is None)) and (self.loadCsvFlag)):
                colNum = 2
            if (not(data is None) and (len(data.text()) > 0)):
                testName=self.uiVar.tableWidget.item(index,0)
                testNumber=self.uiVar.tableWidget.item(index,colNum)
                if len(testNumber.text()) > 0:
                    self.testNoUpdateDict.update({testName.text():testNumber.text()})
                #print(self.testNoUpdateDict)

        result = self.readProgFiles()
        if not(result):
            return
        self.updateTestNumberFiles(self.tnFiles)
        fileList=[]
        for files in self.tnFiles:
            progress_callback.emit(n)
            n=n+1
            if (os.path.exists(files+'.mod'+self.timeStamp)):
                if(files+'.mod' in self.fileCngCntDict.keys()):
                    value1 = self.fileCngCntDict.get(files+'.mod')
                    if not(value1 == 0):
                        self.modifyList = self.modifyList+files+'.mod'+'\n'
                        text=files+'.mod'+self.timeStamp
                        if not(text in fileList):
                            fileList.append(text)
                            self.uiVar.listWidget.insertItem(row,text)
                            row=row+1
                        if (sys.platform == "win32"):
                            command = "Dos2Unix.exe "+files+'.mod'+self.timeStamp
                            subprocess.call(command, shell=True)
                else:
                    os.remove(files+'.mod'+self.timeStamp)
        for n in range(0, 50):
            time.sleep(.05)
            progress_callback.emit(n)
        return

    def updateTestNumberFiles(self,fileNameList):
        localtime = time.localtime(time.time())
        year = str(localtime[0])
        month = str(localtime[1])
        day = str(localtime[2])
        hour = str(localtime[3])
        minute = str(localtime[4])
        second = str(localtime[5])
        self.timeStamp = '.'+year+'_'+month+'_'+day+'_'+hour+'_'+minute+'_'+second
        self.noUpdate = True
        self.fileCngCntDict = {}
        
        for fileName in fileNameList:
            self.changeCount = 0
            if (os.path.exists(fileName)):
##                writePrevilage = os.access(fileName+'.mod'+self.timeStamp, os.W_OK) # Check for write access
##                if not(writePrevilage):
##                    messageDialog = "No write privilages for "+fileName+'.mod'+self.timeStamp+"!"
##                    self.dialogMessageBoxError(messageDialog)
##                    return
                tg = open(fileName, "r",buffering=2)
                tgo = open(fileName+'.mod'+self.timeStamp, "w",buffering=2)
                testGrp = tg.readlines()

                changeComing = False
                for line in testGrp:
                    if('__TestGroup' in line ):
                        tgFinder1 = re.compile('^\s*__TestGroup\s+(\w+)\s+{')
                        findTG1 = re.search(tgFinder1,line)
                        #print("TP1:"+line)
                        #print(findTG1)
                        if (findTG1 and not('/' in line[:20])):
                            #print("TP2:"+line)
                            tgName = findTG1.group(1)
                            if(tgName in self.testNoUpdateDict.keys()):
                               changeComing = True
                               #print("Found Test name to change\n")
                    if((changeComing) and ('__TestID' in line)):
                        tnFinder1 = re.compile('^\s*__TestID\s+=\s+"(\d+)";')
                        findTN1 = re.search(tnFinder1,line)
                        ret = ''
                        if(findTN1):
                            #if( tgName in self.testNoUpdateDict.keys()):
                            try:
                                if not(findTN1.group(1) ==  self.testNoUpdateDict[tgName]) :
                                    ret = re.sub(findTN1.group(1),self.testNoUpdateDict[tgName],line)
                                    changeComing = False
                            except:
                                pass
                        if(len(ret) == 0): 
                            tgo.write(line)
                        else:
                            tgo.write(ret)
                            self.changeCount = self.changeCount + 1
                            self.noUpdate = False
                    else:
                        tgo.write(line)
            if(self.changeCount > 0):
                self.fileCngCntDict.update({fileName+'.mod':self.changeCount})
        tg.close
        tgo.close

        return

    def readProgFiles(self):
        unaDir = self.uiVar.UNALineEdit.text()
        csvDir = self.uiVar.CSVLineEdit.text()
        baseDir = '.'
        subflowDir = ''
        programDir = ''
        self.tnFiles = []
        if (os.path.exists(csvDir)):
            pos = csvDir[::-1].find('/')
            baseDir = (csvDir[:len(csvDir)-pos-1])
        if (os.path.exists(unaDir)):
            pos = unaDir[::-1].find('/')
            baseDir = (unaDir[:len(unaDir)-pos-1])
        for root,dirs,files in os.walk(baseDir):
            for filename in dirs:
                dirFinder1 = re.compile('^(Programs?$)|(Sub[Ff]lows?$)')
                findDIR = re.search(dirFinder1,filename)
                #print("filename "+filename)
                if(findDIR):
                    if(findDIR.group(1)):
                        programDir = findDIR.group(1)
                    if(findDIR.group(2)):
                        subflowDir = findDIR.group(2)
        programDir = baseDir+"/"+programDir+"/"
        for root,dirs,files in os.walk(programDir):
            for filename in files:
                if(filename.startswith("TestGroup")):
                    if(filename.endswith(".uno")):     
                        self.tnFiles.append(programDir+filename)
                    #print(programDir+filename)
        
        flowDir = baseDir+"/"+subflowDir+"/"
        for root,dirs,files in os.walk(flowDir):
            for filename in files:
                if(filename.endswith(".uno")):     
                    self.tnFiles.append(flowDir+filename)
                    #print(flowDir+filename)
        return True

    def checkAccessPrevilages(self):
        unaDir = self.uiVar.UNALineEdit.text()
        csvDir = self.uiVar.CSVLineEdit.text()
        baseDir = '.'
        subflowDir = ''
        programDir = ''
        self.cwdDirs = []
        path= os.getcwd()
        errorFlag = False

        writePrevilage = os.access(path, os.W_OK) # Check for write access
        if not(writePrevilage):
            self.cwdDirs.append(path)
            
        for root,dirs,files in os.walk(path):
            for filename in dirs:
                dirFinder1 = re.compile('^(Programs?$)|(Sub[Ff]lows?$)')
                findDIR = re.search(dirFinder1,filename)
                #print("filename "+filename)
                if(findDIR):
                    if(findDIR.group(1)):
                        programDir = findDIR.group(1)
                    if(findDIR.group(2)):
                        subflowDir = findDIR.group(2)
        programDir = baseDir+"/"+programDir+"/"
        for root,dirs,files in os.walk(programDir):
            for filename in files:
                if(filename.startswith("TestGroup")):
                    if(filename.endswith(".uno")):     
                        self.cwdDirs.append(programDir)
                    #print(programDir+filename)
        
        flowDir = baseDir+"/"+subflowDir+"/"
        for root,dirs,files in os.walk(flowDir):
            for filename in files:
                if(filename.endswith(".uno")):     
                    self.cwdDirs.append(flowDir)
        dirList = list(set(self.cwdDirs))
        listofDir = ''
        for directory in dirList:
            writePrevilage = os.access(directory, os.W_OK) # Check for write access
            readPrevilage = os.access(directory, os.R_OK) # Check for write access
            if not((writePrevilage) and (readPrevilage)):
                listofDir = listofDir + '\n' + directory + ', '
                errorFlag = True
        if(errorFlag):        
            messageDialog = "Insufficient access privilages for : "+listofDir.rstrip(', ')+".  Correct and try again."
            self.dialogMessageBoxError(messageDialog)
        return errorFlag



    
    def clearEntry(self,csvData):
        msgBox = QMessageBox(QMessageBox.Critical, ' ', 'Rest Data? ')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setWindowFlags(QtCore.Qt.WindowTitleHint)
        msgBox.setWindowIcon(QtGui.QIcon(':/newPrefix/images/TNC_Icon.png'))
        msgBox.setIconPixmap(QtGui.QPixmap(':/newPrefix/images/reset4_small.png'))
        ret = msgBox.exec_()
        if ret == QMessageBox.No:
            return

##        for rowIndex in range(self.totalRows+1):
##            for colIndex in range(4):
##                self.uiVar.tableWidget.setItem(rowIndex,colIndex,QTableWidgetItem(None))
##                self.uiVar.tableWidget.item(rowIndex,colIndex).setBackground(QtGui.QColor(250,247,228))
        self.uiVar.tableWidget.clear()
        self.headerColor()
        bg = "QLineEdit {background-color:rgb(239, 239, 239)}"
        self.uiVar.CSVLineEdit.setStyleSheet( bg )
        self.uiVar.UNALineEdit.setStyleSheet( bg )
        self.uiVar.UNALineEdit.setText('UNA_File_Name')
        self.uiVar.CSVLineEdit.setText('CSV_File_Name')
        self.uiVar.FindLineEdit.setText('Search')
        self.uiVar.StatusLabel.setText('Status')
        self.uiVar.FilesModLabel.hide()
        self.uiVar.listWidget.hide()
        self.uiVar.Bin2BinButton.setEnabled(True)
        self.uiVar.GenTestIDButton.setEnabled(True)
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar_2.hide()

        self.dataClear = True
        self.tnFiles = []
        self.testNoUpdateDict = {}
        self.fileCngCntDict = {}
        self.timeStamp = ''
        self.noUpdate = True
        self.dataClear = True
        self.csvDataList =[]
        self.csvLoad=False
        return

    def backgroundTable(self):
        for rowIndex in range(self.totalRows):
            for colIndex in range(3):
                try:
                    data = self.uiVar.tableWidget.item(rowIndex,colIndex)
                    if(data.text()):
                        self.uiVar.tableWidget.setItem(rowIndex,colIndex,QTableWidgetItem(data))
                        self.uiVar.tableWidget.item(rowIndex,colIndex).setBackground(QtGui.QColor(250,247,228))
                    if(colIndex >=2 ):
                        self.uiVar.tableWidget.setItem(rowIndex,colIndex,QTableWidgetItem(str('')))
                        self.uiVar.tableWidget.item(rowIndex,colIndex).setBackground(QtGui.QColor(250,247,228))
                except:
                    pass
        return

    def updateProgressBar(self,value):
        debugPrint = False
        value = value % 8
        if(debugPrint):print("%d%% done" % (value))
        #if((value == 0) or (value > 24)):
        #    return
        value2 = value 
        newValue = value2 % 4
        if(value2 < 4): Direction = True
        if(value2 > 3) and (value2 < 8): Direction = False
        if(debugPrint):print("value2:"+str(value2))
        if(debugPrint):print("Direction:"+str(Direction))
        if(debugPrint):print("newValue:"+str(newValue))
        
        if(Direction):
            self.uiVar.progressBar.setGeometry(QtCore.QRect(135+(newValue*45), 585, 35, 5))
            self.uiVar.progressBar_2.setGeometry(QtCore.QRect(270-(newValue*45), 670, 35, 5))
            if(debugPrint):print("pos:"+str(135+(newValue*44)))
        else:
            self.uiVar.progressBar.setGeometry(QtCore.QRect(270-(newValue*45), 585, 35, 5))
            self.uiVar.progressBar_2.setGeometry(QtCore.QRect(135+(newValue*45), 670, 35, 5))
            if(debugPrint):print("pos:"+str(270-(newValue*44)))

        self.uiVar.progressBar.setValue(100)
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar.show()
        self.uiVar.progressBar_2.setValue(100)
        self.uiVar.progressBar_2.hide()
        self.uiVar.progressBar_2.show()
        self.uiVar.StatusLabel.setText( "Processing")
        return


    def updateProgressBar8(self,value):
        value = value % 16
        debugPrint = False
        if(debugPrint):print("%d%% done" % (value))
        #if((value == 0) or (value > 24)):
        #    return
        value2 = value 
        newValue = value2 % 8
        if(value2 < 8): Direction = True
        if(value2 > 7) and (value2 < 16): Direction = False
        if(debugPrint):("value2:"+str(value2))
        if(debugPrint):print("Direction:"+str(Direction))
        if(debugPrint):print("newValue:"+str(newValue))
        
        if(Direction):
            self.uiVar.progressBar.setGeometry(QtCore.QRect(135+(newValue*22.5), 585, 30, 5))
            self.uiVar.progressBar_2.setGeometry(QtCore.QRect(292.5-(newValue*22.5), 670, 30, 5))
            if(debugPrint):print("pos:"+str(135+(newValue*44)))
        else:
            self.uiVar.progressBar.setGeometry(QtCore.QRect(292.5-(newValue*22.5), 585, 30, 5))
            self.uiVar.progressBar_2.setGeometry(QtCore.QRect(135+(newValue*22.5), 670, 30, 5))
            if(debugPrint):print("pos:"+str(270-(newValue*44)))

        self.uiVar.progressBar.setValue(100)
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar.show()
        self.uiVar.progressBar_2.setValue(100)
        self.uiVar.progressBar_2.hide()
        self.uiVar.progressBar_2.show()
        if('Bin2Bin' in self.process):
            statusMessage =  "BintoBinExtracter\nExecuting"
        elif('GenID' in self.process):
            statusMessage =  "Generate TestID\nProcessing"
        else:
            statusMessage =  "Processing"
        self.uiVar.StatusLabel.setText(statusMessage)
        return

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 200):
            time.sleep(.05)
            progress_callback.emit(n)
            #self.updateProgressBar(n)
            #self.updateProgressBar(n)
        return "Done."

    def executeBinToBinExtracter(self, progress_callback):
        n = 0
        self.uiVar.Bin2BinButton.setEnabled(False)
        self.uiVar.GenTestIDButton.setEnabled(False)
        self.Bin2BinComplete=False
        DebugPrint=False
        if (sys.platform == "linux"):
            progress_callback.emit(n)
            n=n+1
            unaFilename = self.uiVar.UNALineEdit.text()
            unaIndex = unaFilename[::-1].find('/')
            unaFilename = unaFilename[len(unaFilename)-unaIndex:]
            unaIndex = unaFilename.find('.una')
            self.csvFilename = unaFilename[:unaIndex]
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('.tmp_script1')))
            self.basePath = base_path
            if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                self.csvFilename = self.csvFilename+'_TestPlan.csv'
            else:
                self.csvFilename = self.csvFilename+'_BinToBinOutput.csv'
                
            self.uiVar.CSVLineEdit.setText(self.csvFilename)
            if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                argStr = "./.tmp_script1 -C pere -u "+unaFilename
                argStrConsole = "./BinToBinExtract_R2.1_L181106 -C pere -u "+unaFilename
            else:
                argStr = "./.tmp_script1 -u "+unaFilename
                argStrConsole = "./BinToBinExtract_R2.1_L181106 -u "+unaFilename
            
            argStr = "script -c '" + argStr+"' /dev/null"
            argStrConsole = "script -c '" + argStrConsole+"' /dev/null"
            
            progress_callback.emit(n)
            n=n+1
            self.Bin2BinComplete=True
            if(DebugPrint):print(self.basePath)
            if ((os.path.exists(self.csvFilename))) :
                os.rename(self.csvFilename,self.csvFilename+".backup")
            if ((os.path.exists(".tmp_script1"))) :
                os.remove(".tmp_script1")
            if ((os.path.exists(".tmp_script2"))) :
                os.remove(".tmp_script2")

            os.system("ln -s "+base_path+"/.tmp_script1 .tmp_script1")
            progress_callback.emit(n)
            n=n+1
            os.system("ln -s "+base_path+"/.tmp_script2 .tmp_script2")
            for n in range(n, 50):
                time.sleep(.05)
                progress_callback.emit(n)
            process = subprocess.Popen(str(argStr), stdout=subprocess.PIPE,shell = True)
##            os.system(argStr)
##            command="script"
##            t = Timer(10, self.killProcess, [command])
##            t.start()
##            process.wait()
##            t.cancel()
##            progress_callback.emit(n)
##            n=n+1
            self.Bin2BinComplete=False
            while True:
              line = process.stdout.readline()
              if line != b'':
                if(DebugPrint): print(line)
                progress_callback.emit(n)
                n=n+1
                time.sleep(.05)
              else:
                command="script"
                self.killProcess(command)
                break
            #return
            if(self.showConsoleCommand): print("Command Executed: "+argStrConsole)
            for n in range(n, 70):
                time.sleep(.05)
                progress_callback.emit(n)
            if ((os.path.exists(".tmp_script1"))) :
                os.remove(".tmp_script1")
            if ((os.path.exists(".tmp_script2"))) :
                os.remove(".tmp_script2")
        if (sys.platform == "win32"):
            self.uiVar.StatusLabel.setText( "BinToBinExtract Only\n Runs on Linux Systems")
        return


    def csvFileCheck(self,fileCSV):
            CSVFileType = False
            if not((os.path.exists(fileCSV))) :
                return
            fo = open(fileCSV, "r",buffering=2)
            position = fo.tell()
            fileArrayCSV = fo.readlines()
            fo.close()

            for line in fileArrayCSV:
                line = line.replace("\"", "")
                if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
                    if(('Test Num,Test Name,LimitStruct Name,LowLimitA,HighLimitA,Units,LowLimit,HighLimit,HW Bin,BinNameA,SW Bin,FunctionCallAtEnd,FunctionName'  in line ))   :
                        CSVFileType = True
                else:
                    if(('Index,Test Number,Test Group Name,SubFlow,Bin Name,SW Bin,HW Bin,Comments'  in line ))   :
                        CSVFileType = True
                    #print(line)
                    break
            #print(CSVFileType)
            return CSVFileType


    def unaFileCheck(self,fileUNA):
            UNAFileType = False
            if not((os.path.exists(fileUNA))) :
                return
            fo = open(fileUNA, "r",buffering=2)
            position = fo.tell()
            fileArrayUNA = fo.readlines()
            fo.close()
            for line in fileArrayUNA:
                if(('Unison:SyntaxRevision'  in line ))   :
                    UNAFileType = True
                    break
            return UNAFileType
        
    def print_output(self, s):
        debugPrint = False
        if(debugPrint): print(s)


    def Bin2Bin_thread_complete(self):
        debugPrint = False
        if (sys.platform == "win32"):
            return
        if not(self.Bin2BinComplete):
            self.uiVar.StatusLabel.setText( "BinToBinExtract\nHang Issue")
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
            argStr = "\rm "+self.csvFilename
            process = subprocess.Popen(str(argStr), stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
            return
        if(debugPrint): print("THREAD COMPLETE!")
        self.uiVar.StatusLabel.setText( "BinToBinExtract\nComplete")
        csvFile = self.csvFilename
        #if (sys.platform == "win32"):
        #    csvFile ='LEBA0_F_U1709DPGX_A4_BinToBinOutput.csv'
        self.csvLoad = False
        if not((os.path.exists(csvFile))) :
            messageDialog = csvFile+" does not exist.\n Check your source files \
            and run the standalone\nversion of BinToBinExtracter!"
            self.dialogMessageBoxError(messageDialog)
            return
        try:
            self.readCVSToTable(csvFile)
            #self.uiVar.StatusLabel.setText( "        Done")
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
        except:
            self.uiVar.StatusLabel.setText( "BinToBinExtract\nError")
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
            messageDialog = "The BinToBinExtracter has an Error.\n Check your source files \
            and run the standalone\nversion of BinToBinExtracter!"
            self.dialogMessageBoxError(messageDialog)
            argStr = "\rm "+self.csvFilename
            process = subprocess.Popen(str(argStr), stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
            pass
        self.uiVar.Bin2BinButton.setEnabled(True)
        self.uiVar.GenTestIDButton.setEnabled(True)

        return
    
    def GenID_thread_complete(self):
        debugPrint = False        
        if((self.noUpdate ) and (self.loadCsvFlag)):
            self.dialogMessageBoxWarning("TestID's Are Identical")
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
            self.uiVar.StatusLabel.setText('Status')
            self.uiVar.Bin2BinButton.setEnabled(True)
            self.uiVar.GenTestIDButton.setEnabled(True)
            return
        if((self.noUpdate ) and not(self.loadCsvFlag)):
            self.dialogMessageBoxWarning('No TestID Update in Table to Generate?!')
            self.uiVar.progressBar.hide()
            self.uiVar.progressBar_2.hide()
            self.uiVar.StatusLabel.setText('Status')
            self.uiVar.Bin2BinButton.setEnabled(True)
            self.uiVar.GenTestIDButton.setEnabled(True)
            return
        if(debugPrint): print("THREAD COMPLETE!")
        self.uiVar.StatusLabel.setText( "TestID Generation\nComplete")
        self.uiVar.progressBar.hide()
        self.uiVar.progressBar_2.hide()
        if not(self.noUpdate):
            self.uiVar.listWidget.show()
            self.uiVar.FilesModLabel.show()
        self.uiVar.Bin2BinButton.setEnabled(True)
        self.uiVar.GenTestIDButton.setEnabled(True)
        return
		
    def Bin2Bin_ThreadRunner(self):
        result = self.checkAccessPrevilages()
        if(result):
            return
        self.custKEY = self.uiVar.KEYLineEdit.text()
        self.custKEY.replace(" ", "")
        self.process = 'Bin2Bin'
        self.loadCsvFlag = False

        if(("pere" in self.custKEY) and (len(self.custKEY) == 4)):
             donothing = 1
        elif((len(self.custKEY) > 0)):
            messageDialog = "Customizaion Key is Invalid."
            self.dialogMessageBoxError(messageDialog)
            self.uiVar.KEYLineEdit.setText("")
            return
        else:
            pass
        fileOK = self.UNAFileSelect()
        if(self.FileCanel):
            return
        if not(fileOK):
            self.uiVar.StatusLabel.setText( "UNA File Type Issue")
            return
        # Pass the function to execute
        #self.initProgressBar()
        #worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker = Worker(self.executeBinToBinExtracter) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.Bin2Bin_thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        worker.signals.progress.connect(self.updateProgressBar8)
        # Execute
        try:
            self.threadpool.start(worker)
        except:
            pass
            self.uiVar.Bin2BinButton.setEnabled(True)
            self.uiVar.GenTestIDButton.setEnabled(True)
        return
        
    def GenID_ThreadRunner(self):
        self.process = 'GenID'
        status = self.cellCheck()
        if(status):
            return
        # Pass the function to execute
        #worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker = Worker(self.updateTableData) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.GenID_thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        worker.signals.progress.connect(self.updateProgressBar8)
        # Execute
        self.threadpool.start(worker)
        return

    
if __name__ == '__main__':
    color_list=['green','blue']
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion')) # won't work on windows style.

    # Create and display the splash screen
    splash_pix = QPixmap(':/newPrefix/images/TNCSplash1.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    progressBar = QProgressBar(splash)

    splash.setMask(splash_pix.mask())
    splash.show()
    for i in range(0, 10):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
           app.processEvents()

    # Simulate something that takes time
    
    window = TNCToolWindow()
    splash.finish(window)
    window.setStyleSheet("background-image:url(:/newPrefix/images/Circuit13.jpg)")
    if (sys.platform == "linux"):
        try:
            envVar = os.environ["QT_XKB_CONFIG_ROOT"]
        except:
            print("Environment QT_XKB_CONFIG_ROOT not set.")
            window.env_var()
            sys.exit(app.exec_())
            pass
    window.show()
    sys.exit(app.exec_())
