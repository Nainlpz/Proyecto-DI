from PyQt6 import QtCore

from conexion import *
from events import Events

class Products:

    @staticmethod
    def cargaFamilypro():
        datos = ["", "Foods", "Furniture", "Clothes", "Electronics"]
        globals.ui.cmbFamily.clear()
        globals.ui.cmbFamily.addItems(datos)

    @staticmethod
    def loadTableProducts():
        try:
            listTabProducts = Conexion.listProducts()
            index = 0
            for record in listTabProducts:
                globals.ui.tblProductList.setRowCount(index + 1)
                globals.ui.tblProductList.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblProductList.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblProductList.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  " + str(record[2]) + "  ")))
                globals.ui.tblProductList.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblProductList.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[4]) + " €"))

                globals.ui.tblProductList.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblProductList.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblProductList.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblProductList.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight.AlignRight)
                globals.ui.tblProductList.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight.AlignRight)

                index += 1

        except Exception as error:
            print("error en loadTableProducts ", error)

    @staticmethod
    def selectProduct():
        try:
            row = globals.ui.tblProductList.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneProduct(str(data[0]))
            boxes = [globals.ui.txtCode, globals.ui.textNameProduct, globals.ui.txtStock]

            for i in range(len(boxes)):
                boxes[i].setText(str(record[i]))

            globals.ui.txtUnitPrice.setText(str(record[4]))
            globals.ui.cmbFamily.setCurrentText(record[3])

        except Exception as error:
            print("error en selectProduct", error)

    @staticmethod
    def saveProduct():
        try:
            newProduct = [globals.ui.textNameProduct.text(), globals.ui.txtStock.text(),
                      globals.ui.cmbFamily.currentText(), globals.ui.txtUnitPrice.text()]

            if Conexion.addProduct(newProduct) and len(newProduct) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Product Added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, Unfilled data \n"
                             "Contact with the administrator or try again later.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    mbox.hide()

            Products.loadTableProducts()

        except Exception as error:
            print("error saveProduct", error)

    @staticmethod
    def delProduct():
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec():
                code = globals.ui.txtCode.text()
                if Conexion.deleteProduct(code):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Product")
                else:
                    print("Algo ha ido mal")
                Products.loadTableProducts()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error. Contact with the administrator or try again later.")


        except Exception as error:
            print("error en delProduct", error)

    @staticmethod
    def modifyProduct():
        try:
            if globals.ui.txtCode.text() != "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Modify Data")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Are you sure modify all data?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    id = globals.ui.txtCode.text()
                    modProduct = [globals.ui.textNameProduct.text(), globals.ui.cmbFamily.currentText(),
                              globals.ui.txtStock.text(), globals.ui.txtUnitPrice.text()
                              ]

                    if Conexion.modifyProduct(id, modProduct):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Information")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setText("Product modified")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error modifying data. Empty Data? ")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

            Products.loadTableProducts()

        except Exception as error:
            print("error modify pro ", error)

    @staticmethod
    def cleanProduct():
        try:
            boxes = [globals.ui.txtCode, globals.ui.textNameProduct,
                     globals.ui.txtStock, globals.ui.txtUnitPrice]

            for i in range(len(boxes)):
                boxes[i].setText("")

            globals.ui.cmbFamily.setCurrentText("")

        except Exception as error:
            print("error clean pro ", error)

    @staticmethod
    def comaPunto(valor):
        try:
            valor = valor.replace(",", ".")
            globals.ui.txtUnitPrice.setText(valor)
        except Exception as error:
            print("error comaPunto", error)