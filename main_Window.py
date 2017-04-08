# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_Window.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql
from main import delete_all_db, exit_update_db

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(790, 686)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_5.addWidget(self.line)
        self.label = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("emblems/emblem-web.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon, _fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("emblems/emblem-mail.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon1, _fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("emblems/emblem-readonly.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon2, _fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("emblems/emblem-system-symbolic.symbolic.png")), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.comboBox.addItem(icon3, _fromUtf8(""))
        self.verticalLayout_5.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 658, 509))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.modelView = QtGui.QTableView(self.scrollAreaWidgetContents)
        self.modelView.setGeometry(QtCore.QRect(10, 50, 661, 471))
        self.modelView.setMaximumSize(QtCore.QSize(555555, 16777215))
        self.modelView.setObjectName(_fromUtf8("modelView"))
        self.modelView.setAutoScroll(True)
        self.modelView.setFixedWidth(500)
        self.modelView.setMinimumWidth(1000)
        ##
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('test.db')
        self.model = QtSql.QSqlTableModel()
        self.modelView.setModel(self.model)
        self.modelView.setColumnHidden(1, True)
        self.model.setTable('INTERNET')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "URL")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Username")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Password")

        self.newRow_button = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.newRow_button.setGeometry(QtCore.QRect(10, 10, 90, 28))
        self.newRow_button.setObjectName(_fromUtf8("newRow_button"))
        self.newRow_button.clicked.connect(lambda: self.addrow(self.model))

        self.deleteRow_button = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.deleteRow_button.setGeometry(QtCore.QRect(110, 10, 90, 28))
        self.deleteRow_button.setObjectName(_fromUtf8("deleteRow_button"))
        self.deleteRow_button.clicked.connect(lambda: self.model.removeRow(self.modelView.currentIndex().row()))

        self.deleteDB_button = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.deleteDB_button.setGeometry(QtCore.QRect(220, 10, 151, 28))
        self.deleteDB_button.setObjectName(_fromUtf8("deleteDB_button"))
        self.deleteDB_button.clicked.connect(lambda: self.delete_all())
        ##
        self.line_2 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(0, 10, 662, 3))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.modelView.raise_()
        self.line_2.raise_()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def delete_all(self):
        delete_all_db()
        self.model.clear()
        self.modelView.reset()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Honey Encryption", "Honey Encryption", None))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">   Groups Select   </span></p></body></html>",
                                      None))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; color:#00007f;\">Honey Encryption Locker</span></p></body></html>",
                                        None))
        self.comboBox.setItemText(0, _translate("MainWindow", "Internet", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Emails", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "PINS", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "Others", None))
        self.newRow_button.setText(_translate("MainWindow", "New Row", None))
        self.deleteRow_button.setText(_translate("MainWindow", "Delete Row", None))
        self.deleteDB_button.setText(_translate("MainWindow", "Delete Database", None))

        self.comboBox.activated[str].connect(self.changetable)  # switches

    # def __del__(self):
    #     exit_update_db()
    def closeEvent(self, event):
        print("event")
        exit_update_db()
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def changetable(self, text):
        text = str(text)
        if text == "Internet":
            self.modelView.reset()
            self.modelView.setModel(self.model)
            self.model.clear()
            self.model.setTable('INTERNET')
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.model.select()
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "URL")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Username")
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Password")
            self.modelView.reset()
            self.modelView.setModel(self.model)
        elif text == "Emails":
            self.model.clear()
            self.model.setTable('EMAILS')
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.model.select()
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "URL")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Username")
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Password")
            self.modelView.reset()
            self.modelView.setModel(self.model)
        elif text == "PINS":
            self.model.clear()
            self.model.setTable('PINS')
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.model.select()
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "URL")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Password")
            self.modelView.reset()
            self.modelView.setModel(self.model)
        elif text == "Others":
            self.model.clear()
            self.model.setTable('OTHERS')
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.model.select()
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "URL")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Username")
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Password")
            self.modelView.reset()
            self.modelView.setModel(self.model)

    def addrow(self, model):
        print(self.model.rowCount())
        ret = self.model.insertRows(model.rowCount(), 1)
        print(ret)
