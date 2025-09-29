from PyQt6 import QtWidgets
import sys

from conexion import Conexion
from customers import *
from venAux import Calendar
from window import Ui_MainWindow
from events import *
import globals


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # Instance
        globals.vencal = Calendar()

        # Conexion
        Conexion.db_conexion(self)

        # Funciones de menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        # Funciones de line edit
        globals.ui.txtDniCif.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtNameCli.text(), globals.ui.txtNameCli))
        globals.ui.txtSurnameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtSurnameCli.text(), globals.ui.txtSurnameCli))
        globals.ui.txtEmailCli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailCli.text()))
        globals.ui.txtMobileCli.editingFinished.connect(lambda: Customers.checkMobile(globals.ui.txtMobileCli.text()))

        # Funciones combobox
        Events.loadProv(self)
        globals.ui.cmbProvinceCli.currentIndexChanged.connect(Events.loadMuni)


        # Funciones buttons
        globals.ui.btnDateCli.clicked.connect(Events.openCalendar)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())