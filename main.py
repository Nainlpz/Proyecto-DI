from PyQt6 import QtWidgets
import sys

from conexion import Conexion
from customers import *
from products import Products
from reports import *
from venAux import *
from window import Ui_MainWindow
from events import *
import globals
import styles

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # Instance
        globals.vencal = Calendar()
        globals.about = About()
        globals.dlgOpen = FileDialogOpen()
        self.reports = Reports()

        # Styles
        app.setStyleSheet(styles.load_stylesheet())

        # Conexion
        varCli = True
        Conexion.db_conexion(self)
        Customers.loadTableCli(varCli)
        Products.loadTableProducts()
        Events.resizeTabCustomer(self)

        # Como cargar un combo desde un array
        family = ["Foods", "Furniture", "Clothes", "Electronic"]
        globals.ui.cmbFamily.addItems(family)

        # Functions menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.openAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestoreBackup.triggered.connect(Events.restoreBackup)
        globals.ui.actionCustomers.triggered.connect(Events.exportXlsCustomers)
        globals.ui.actionCustomer_Report.triggered.connect(self.reports.reportCustomers)

        # Functions line edit
        globals.ui.txtDniCif.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtNameCli.text(), globals.ui.txtNameCli))
        globals.ui.txtSurnameCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtSurnameCli.text(), globals.ui.txtSurnameCli))
        globals.ui.txtAddressCli.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtAddressCli.text(), globals.ui.txtAddressCli))
        globals.ui.txtEmailCli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailCli.text()))
        globals.ui.txtMobileCli.editingFinished.connect(lambda: Customers.checkMobile(globals.ui.txtMobileCli.text()))

        # Functions Historical
        globals.ui.chcHistorical.stateChanged.connect(Customers.HistoricalCli)

        # Functions combobox
        Events.loadProv(self)
        globals.ui.cmbProvinceCli.currentIndexChanged.connect(Events.loadMuni)


        # Functions buttons
        globals.ui.btnDateCli.clicked.connect(Events.openCalendar)
        globals.ui.btnDeleteCli.clicked.connect(Customers.delClient)
        globals.ui.btnSaveCli.clicked.connect(Customers.saveClient)
        globals.ui.btnReload.clicked.connect(Customers.reloadClient)
        globals.ui.btnModifyCli.clicked.connect(Customers.modifyClient)
        globals.ui.btnSearchDni.clicked.connect(Customers.searchClient)

        globals.ui.btnSaveProduct.clicked.connect(Products.saveProduct)
        globals.ui.btnDeleteProduct.clicked.connect(Products.delProduct)

        # Functions tables
        globals.ui.tblCustomerList.clicked.connect(Customers.selectCustomer)
        globals.ui.tblProductList.clicked.connect(Products.selectProduct)
        
        # Functions
        Events.loadStatusBar(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())