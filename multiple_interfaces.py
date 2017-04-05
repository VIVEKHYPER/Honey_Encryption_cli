import os.path
import sys

from Create import Ui_Form2
from HE import Ui_Form
from PyQt4 import QtGui


class LoginWidget(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class CreateWidget(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form2()
        self.ui.setupUi(self)


if __name__ == "__main__":
    if os.path.isfile("test.db"):  # Checks whether there is file named test.db
        app = QtGui.QApplication(sys.argv)
        myapp = LoginWidget()
        myapp.show()
    else:
        app = QtGui.QApplication(sys.argv)
        myapp = CreateWidget()
        myapp.show()

sys.exit(app.exec_())
