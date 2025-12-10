from PyQt6 import QtWidgets
import sys

from PyQt6.QtGui import QShortcut, QKeySequence, QKeyEvent

from conexion import Conexion
from customers import *
from products import Products
from reports import *
from venAux import *
from window import Ui_MainWindow
from events import *
import globals
import styles
from invoice import Invoice

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
        self.invoice = Invoice()

        # Styles
        app.setStyleSheet(styles.load_stylesheet())

        # Conexion
        varCli = True
        Conexion.db_conexion(self)
        Customers.loadTableCli(varCli)
        Products.loadTableProducts()
        Events.resizeTabCustomer(self)
        Events.resizeTabProducts()
        Events.resizeTableSales()
        Products.cargaFamilypro()
        Products.loadTableProducts()
        Invoice.loadTableInvoice()
        Invoice.loadInvoiceirst()

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

        globals.ui.txtUnitPrice.editingFinished.connect(lambda: Products.comaPunto(globals.ui.txtUnitPrice.text()))
        globals.ui.textNameProduct.editingFinished.connect(lambda: Customers.capLetter(globals.ui.textNameProduct.text(), globals.ui.textNameProduct))
        globals.ui.txtCode.setEnabled(False)
        globals.ui.txtCode.setStyleSheet('background-color: rgb(255, 255, 197);')

        globals.ui.txtDniFactura.editingFinished.connect(Invoice.searchInvoice)
        globals.ui.txtDniFactura.editingFinished.connect(lambda: Customers.capLetter(globals.ui.txtDniFactura.text(), globals.ui.txtDniFactura))

        # Functions Historical
        globals.ui.chcHistorical.stateChanged.connect(Customers.HistoricalCli)

        # Functions combobox
        Events.loadProv(self)
        globals.ui.cmbProvinceCli.currentIndexChanged.connect(Events.loadMuni)

        # Eventos teclado
        self.scCleanFac = QtGui.QShortcut(QKeySequence("Ctrl+S"), self)
        self.scCleanFac.activated.connect(Invoice.saveSales)

        # Functions buttons
        globals.ui.btnDateCli.clicked.connect(Events.openCalendar)
        globals.ui.btnDeleteCli.clicked.connect(Customers.delClient)
        globals.ui.btnSaveCli.clicked.connect(Customers.saveClient)
        globals.ui.btnReload.clicked.connect(Customers.reloadClient)
        globals.ui.btnModifyCli.clicked.connect(Customers.modifyClient)
        globals.ui.btnSearchDni.clicked.connect(Customers.searchClient)

        globals.ui.btnSaveProduct.clicked.connect(Products.saveProduct)
        globals.ui.btnDeleteProduct.clicked.connect(Products.delProduct)
        globals.ui.btnModifyProduct.clicked.connect(Products.modifyProduct)
        globals.ui.btnReloadProducts.clicked.connect(Products.cleanProduct)

        globals.ui.btnReloadFactura.clicked.connect(Invoice.reloadInvoice)
        globals.ui.btnSaveFactura.clicked.connect(Invoice.saveInvoice)
        globals.ui.btnSaveSale.clicked.connect(Invoice.saveSales)


        # Functions tables
        globals.ui.tblCustomerList.clicked.connect(Customers.selectCustomer)
        globals.ui.tblProductList.clicked.connect(Products.selectProduct)
        globals.ui.tblFactura.clicked.connect(Invoice.selectInvoice)
        globals.ui.tblSales.itemChanged.connect(Invoice.cellChangedSales)
        
        # Functions
        Events.loadStatusBar(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())