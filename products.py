from PyQt6 import QtCore

from conexion import *
from events import Events

class Products:

    @staticmethod
    def loadTableProducts():
        try:
            listTabProducts = Conexion.listProducts()
            index = 0
            for record in listTabProducts:
                globals.ui.tblProductList.setRowCount(index + 1)
                globals.ui.tblProductList.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblProductList.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblProductList.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tblProductList.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblProductList.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[4])))

                globals.ui.tblCustomerList.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerList.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerList.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)

                index += 1

        except Exception as error:
            print("error en loadTableProducts", error)

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
            newProduct = [globals.ui.txtCode.text(), globals.ui.textNameProduct.text(), globals.ui.txtStock.text(),
                      globals.ui.cmbFamily.currentText(), globals.ui.txtUnitPrice.text()]

            if Conexion.addProduct(newProduct):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Product Added")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, Product exists")

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