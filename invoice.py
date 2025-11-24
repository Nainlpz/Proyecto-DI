from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTabWidget

from conexion import Conexion
import globals
from datetime import datetime

class Invoice:

    @staticmethod
    def searchInvoice():
        try:
            dni = globals.ui.txtDniFactura.text().upper().strip()
            if dni == "" or Conexion.searchClient(dni):
                if dni == "":
                    dni = "00000000T"
                    globals.ui.txtDniFactura.setText(dni)
                record = Conexion.dataOneCustomer(dni)
                globals.ui.lblNameFactura.setText(record[2] + " " + record[3])
                globals.ui.lblFacturaType.setText(record[9])
                globals.ui.lblAddressFactura.setText(record[6] + "   " + record[8] + "   " + record[7])
                globals.ui.lblMobileFactura.setText(str(record[5]))
                if record[10] == "True":
                    globals.ui.lblStatusFactura.setText("Activo")
                else:
                    globals.ui.lblStatusFactura.setText("Inactivo")

            else:
                globals.ui.txtDniFactura.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Client not exists")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
        except Exception as error:
            print("error en saveInvoice", error)

    @staticmethod
    def reloadInvoice():
        try:
            formfact = [globals.ui.lblNameFactura, globals.ui.lblAddressFactura, globals.ui.lblStatusFactura,
                      globals.ui.lblFacturaType, globals.ui.lblMobileFactura, globals.ui.lblFechaFactura,
                      globals.ui.lblNumFactura, globals.ui.txtDniFactura]

            for i, dato in enumerate(formfact):
                formfact[i] = dato.setText("")

        except Exception as error:
            print("error en reloadClient", error)

    @staticmethod
    def saveInvoice():
        try:
            dni = globals.ui.txtDniFactura.text()
            data = datetime.now().strftime("%d/%m/%Y")
            if dni != "" and data != "":
                Conexion.insertInvoice(dni, data)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en saveInvoice", error)