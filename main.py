from PyQt6 import QtWidgets
import sys

from conexion import Conexion
from customers import *
from venAux import *
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
        globals.about = About()

        # Conexion
        varCli = True
        Conexion.db_conexion(self)
        Customers.loadTableCli(varCli)
        Events.resizeTabCustomer(self)

        # Funcions menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)

        # Funcions line edit
        globals.ui.txtDniCif.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtNameCli.text(), globals.ui.txtNameCli))
        globals.ui.txtSurnameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtSurnameCli.text(), globals.ui.txtSurnameCli))
        globals.ui.txtAddressCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtAddressCli.text(), globals.ui.txtAddressCli))
        globals.ui.txtEmailCli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailCli.text()))
        globals.ui.txtMobileCli.editingFinished.connect(lambda: Customers.checkMobile(globals.ui.txtMobileCli.text()))

        # Funtions Historial
        globals.ui.chcHistorical.stateChanged.connect(Customers.HistoricalCli)

        # Funcions combobox
        Events.loadProv(self)
        globals.ui.cmbProvinceCli.currentIndexChanged.connect(Events.loadMuni)


        # Funcions buttons
        globals.ui.btnDateCli.clicked.connect(Events.openCalendar)
        globals.ui.btnDeleteCli.clicked.connect(Customers.delClient)
        globals.ui.btnSaveCli.clicked.connect(Customers.saveClient)

        # Funcions tables
        globals.ui.tblCustomerList.clicked.connect(Customers.selectCustomer)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())