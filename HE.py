# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HE.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from PyQt4 import QtGui
from fake_Window import Ui_FakeWindow
from main import log_in, exit_update_db
from main_Window import Ui_MainWindow


class MyMainWindow(QtGui.QMainWindow, Ui_MainWindow):  # Main Window which views entire database
    def __init__(self, parent=None):  # Initializing main window class in qt
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


class MyFakeWindow(QtGui.QMainWindow, Ui_FakeWindow):  # Fake Window which views fake database
    def __init__(self, parent=None):  # Initializing main window class in qt
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_FakeWindow()
        self.ui.setupUi(self)


from PyQt4 import QtCore, QtGui

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


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(666, 533)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.newButton = QtGui.QPushButton(Form)
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.verticalLayout.addWidget(self.newButton)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_11.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 25))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_5.addWidget(self.lineEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 25))
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Honey Encryption ", None))
        self.newButton.setText(_translate("Form", "Create New Key Database", None))
        self.label.setText(_translate("Form",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Database Log In</span></p></body></html>",
                                      None))
        self.label_2.setText(_translate("Form",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Username</span></p></body></html>",
                                        None))
        self.label_3.setText(_translate("Form",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Password</span></p></body></html>",
                                        None))
        self.pushButton.setText(_translate("Form", "Abort", None))
        self.pushButton_2.setText(_translate("Form", "Login", None))
        self.pushButton_2.clicked.connect(
            lambda: self.onClick(Form))  # uses lambdda function# activates onClick function when button is clicked

    def onClick(self, Form):
        username = self.lineEdit.text()  # Reads username from lineEdit
        password = self.lineEdit_2.text()  # Reads password from lineEdit
        try:
            access = log_in(username, password)  # Login to database and returns access value as '1' if it is success
        except (ValueError, AttributeError):
            exit_update_db()
            access = log_in(username, password)

        if access == 1:
            self.myapp1 = MyMainWindow()  # opens main window if access is 1
            self.myapp1.show()
        else:
            self.myapp1 = MyFakeWindow()  # opens fake window if access is 0
            self.myapp1.show()
        Form.close()
