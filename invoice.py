from operator import index
from time import sleep

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTabWidget

from conexion import Conexion
import globals
from datetime import datetime
from PyQt6 import QtCore
from time import sleep

from globals import linesales


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
                if Conexion.insertInvoice(dni, data):
                    Invoice.loadTableInvoice()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Invoice")
                    mbox.setText("Invoice created successfully")
                    if mbox.exec():
                        mbox.hide()
                    Invoice.activeSales()

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

    @staticmethod
    def loadTableInvoice():
        try:
            records = Conexion.allInvoices()
            index = 0
            for record in records:

                globals.ui.tblFactura.setRowCount(index + 1)

                globals.ui.tblFactura.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblFactura.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblFactura.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                globals.ui.tblFactura.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblFactura.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblFactura.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)

                index += 1

            datos = records[0]
            globals.ui.lblNumFactura.setText(str(datos[0]))
            globals.ui.txtDniFactura.setText(str(datos[1]))
            globals.ui.lblFechaFactura.setText(str(datos[2]))

        except Exception as error:
            print("error en loadTableInvoice", error)

    @staticmethod
    def loadInvoiceirst():
        try:
            globals.ui.txtDniFactura.setText("00000000T")
            globals.ui.lblNumFactura.setText("")
            globals.ui.lblFechaFactura.setText("")
            Invoice.searchInvoice()

        except Exception as error:
            print("error en loadInvoiceirst", error)

    @staticmethod
    def selectInvoice():
        try:
            row = globals.ui.tblFactura.selectedItems()
            data = [dato.text() for dato in row]
            recordinvoice = Conexion.dataOneInvoice(str(data[0]))
            Invoice.cargarVentas(str(data[0]))
            boxes = [globals.ui.lblNumFactura, globals.ui.txtDniFactura, globals.ui.lblFechaFactura]

            for i in range(len(boxes)):
                boxes[i].setText(str(recordinvoice[i]))

        except Exception as error:
            print("error en selectInvoice", error)

    @staticmethod
    def activeSales(row=None):
        try:
            if row is None:
                row = 0

            if row >= globals.ui.tblSales.rowCount():
                globals.ui.tblSales.setRowCount(row + 1)

            center_align = QtCore.Qt.AlignmentFlag.AlignCenter

            # Column 0 (Code)
            item_code = QtWidgets.QTableWidgetItem("")
            item_code.setTextAlignment(center_align)
            globals.ui.tblSales.setItem(row, 0, item_code)

            # Column 1 (Concept)
            globals.ui.tblSales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))

            # Column 2 (Price)
            item_price = QtWidgets.QTableWidgetItem("")
            item_price.setTextAlignment(center_align)
            globals.ui.tblSales.setItem(row, 2, item_price)

            # Column 3 (Quantity)
            item_qty = QtWidgets.QTableWidgetItem("")
            item_qty.setTextAlignment(center_align)
            globals.ui.tblSales.setItem(row, 3, item_qty)

            # Column 4 (Total)
            item_total = QtWidgets.QTableWidgetItem("")
            item_total.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            globals.ui.tblSales.setItem(row, 4, item_total)

        except Exception as error:
            print("error en activeSales", error)

    @staticmethod
    def cellChangedSales(item):

        try:
            if item is None:
                return

            row = item.row()
            col = item.column()

            if col not in (0, 3):
                return

            globals.ui.tblSales.blockSignals(True)

            value = item.text().strip()

            if col == 0:
                if value == "":
                    globals.ui.tblSales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
                    globals.ui.tblSales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
                else:
                    data = Conexion.selectProduct(value)
                    if data:
                        globals.ui.tblSales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                        globals.ui.tblSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                        globals.ui.tblSales.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setWindowTitle("Warning")
                        mbox.setText("Product not exists")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                            mbox.hide()
                        globals.ui.tblSales.setItem(row, 0, QtWidgets.QTableWidgetItem(""))

            if col in (0, 3):
                item_qty = globals.ui.tblSales.item(row, 3)
                item_price = globals.ui.tblSales.item(row, 2)

                if item_qty and item_price:
                    try:
                        cantidad = float(item_qty.text())
                        precio = float(item_price.text())
                        tot = round(precio * cantidad, 2)

                        globals.ui.tblSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                        globals.ui.tblSales.item(row, 4).setTextAlignment(
                            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    except ValueError:
                        globals.ui.tblSales.setItem(row, 4, QtWidgets.QTableWidgetItem("0.00"))

            grand_subtotal = 0.0

            for r in range(globals.ui.tblSales.rowCount()):
                item_total = globals.ui.tblSales.item(r, 4)
                if item_total and item_total.text():
                    try:
                        grand_subtotal += float(item_total.text())
                    except ValueError:
                        pass

            globals.subtotal = grand_subtotal
            iva = 0.21
            totaliva = round(globals.subtotal * iva, 2)
            total = round(globals.subtotal + totaliva, 2)

            globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{totaliva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")

            row_items = [globals.ui.tblSales.item(row, i) for i in range(5)]
            is_row_complete = all(it and it.text().strip() for it in row_items)

            if is_row_complete:
                if row == globals.ui.tblSales.rowCount() - 1:
                    next_row = globals.ui.tblSales.rowCount()
                    QtCore.QTimer.singleShot(0, lambda: Invoice.activeSales(next_row))
                    sale = [int(globals.ui.lblNumFactura.text()), int(row_items[0].text()), row_items[1].text(), float(row_items[2].text()),
                              int(row_items[3].text()), float(row_items[4].text())]
                    globals.linesales.append(sale)

        except Exception as error:
            print("Error in cellChangedSales:", error)

        finally:
            globals.ui.tblSales.blockSignals(False)

    @staticmethod
    def saveSales():
        try:
            correct = False
            for data in globals.linesales:
                correct = Conexion.saveSales(data)
            if globals.linesales[-1] and correct:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Sales Saved")
                mbox.setText("Sales saved. Printing Invoice...")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    print("Imprimiendo factura")
                    Invoice.bloquearTablaSales()
                    globals.linesales.clear()
                    globals.ui.tblSales.setRowCount(0)
                    mbox.hide()

        except Exception as error:
            print("Error in saveSales:", error)

    @staticmethod
    def cargarVentas(idfac):
        try:
            data = Conexion.dataOneSale(idfac)
            table = globals.ui.tblSales
            table.setRowCount(0)

            if not data:
                Invoice.activeSales()
            else:
                table.setRowCount(len(data))

                for row_index, sale_row in enumerate(data):
                    for col_index, cell_value in enumerate(sale_row):
                        table_item = QtWidgets.QTableWidgetItem(str(cell_value))
                        table.setItem(row_index, col_index, table_item)

                Invoice.bloquearTablaSales()

        except Exception as error:
            print("Error en cargarVentas:", error)


    @staticmethod
    def bloquearTablaSales():
        try:
            table = globals.ui.tblSales
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        except Exception as error:
            print("Error en bloquearTablaSales:", error)