import re

from PyQt6 import QtCore

import events
import globals
from conexion import *
from events import Events


class Customers:
    @staticmethod
    def checkDni(self=None):
        """

        Módulo para checkear el DNI
        :param self: None
        :type self: None

        """
        try:
            globals.ui.txtDniCif.editingFinished.disconnect(Customers.checkDni)
            dni = globals.ui.txtDniCif.text()
            dni = str(dni).upper()
            globals.ui.txtDniCif.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.txtDniCif.setStyleSheet('background-color: rgb(255, 255, 220);')
                else:
                    globals.ui.txtDniCif.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDniCif.setText(None)
                    #globals.ui.txtDniCif.setFocus()
            else:
                globals.ui.txtDniCif.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDniCif.setText(None)
                #globals.ui.txtDniCif.setFocus()

        except Exception as error:
            print("error en validar dni ", error)

        finally:
            globals.ui.txtDniCif.editingFinished.connect(Customers.checkDni)

    def capLetter(text, widget):
        """

        Modulo para capitalizar el texto de los input
        :param widget: texto y widget input
        :type widget: basestring y widger inpur

        """
        try:
            text = text.title()
            widget.setText(text)
        except Exception as error:
            print("error al capitalizar texto ", error)

    @staticmethod
    def checkEmail(email):
        """

        Modulo para checkear el email con expresión regular
        :param email: correo electronico
        :type email: basestring
        """
        try:
            globals.ui.txtDniCif.editingFinished.disconnect(Customers.checkEmail)
            regex = r'[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(regex, email):
                globals.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                globals.ui.txtEmailCli.setStyleSheet('background-color: #FFC0CB;')
                globals.ui.txtEmailCli.setText(None)
                globals.ui.txtEmailCli.setPlaceholderText("Invalid Email")
                #globals.ui.txtEmailCli.setFocus()
        except Exception as error:
            print("error en validar email ", error)
        finally:
            globals.ui.txtEmailCli.editingFinished.connect(Customers.checkEmail)

    @staticmethod
    def checkMobile(number):
        """

        Modulo para checkear el movil segun la legislacion española
        :param number: nº movil cliente
        :type number: basestring

        """
        try:
            globals.ui.txtDniCif.editingFinished.disconnect(Customers.checkMobile)
            regex = r'^[67]\d{8}$'
            if re.match(regex, number):
                globals.ui.txtMobileCli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                globals.ui.txtMobileCli.setStyleSheet('background-color: #FFC0CB;')
                globals.ui.txtMobileCli.setText(None)
                globals.ui.txtMobileCli.setPlaceholderText("Invalid Mobile")
                #globals.ui.txtMobileCli.setFocus()
        except Exception as error:
            print("error en validar mobile ", error)
        finally:
            globals.ui.txtDniCif.editingFinished.connect(Customers.checkMobile)

    @staticmethod
    def reloadClient():
        """

        Modulo para vaciar el formulario del cliente

        """
        try:
            formcli = [globals.ui.txtDniCif, globals.ui.txtDateCli, globals.ui.txtSurnameCli,
                      globals.ui.txtNameCli, globals.ui.txtEmailCli, globals.ui.txtMobileCli,
                      globals.ui.txtAddressCli]

            for i, dato in enumerate(formcli):
                formcli[i] = dato.setText("")
            Events.loadProv(self = None)
            globals.ui.txtDniCif.setEnabled(True)
            globals.ui.cmbCityCli.clear()
            globals.ui.rdbFactureOnline.setChecked(True)
            globals.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.txtDniCif.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.txtMobileCli.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.lblWarning.setStyleSheet('background-color: rgb(244, 246, 248);')
            globals.ui.lblWarning.setText("")

        except Exception as error:
            print("error en reloadClient", error)

    @staticmethod
    def loadTableCli(varCli):
        """

        Modulo para cargar la tabla clientes
        :param varCli: indica si quiero todos los usuarios o solo activos
        :type varCli: bool

        """
        try:
            listTabCustomers = Conexion.listCustomers(varCli)
            #print(listTabCustomers)
            index = 0
            for record in listTabCustomers:
                globals.ui.tblCustomerList.setRowCount(index + 1)
                globals.ui.tblCustomerList.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tblCustomerList.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblCustomerList.setItem(index, 2, QtWidgets.QTableWidgetItem((" " + str(record[5]) + " ")))
                globals.ui.tblCustomerList.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tblCustomerList.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tblCustomerList.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                if str(record[10]) == "True":
                    globals.ui.tblCustomerList.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.tblCustomerList.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))
                globals.ui.tblCustomerList.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerList.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerList.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerList.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error en loadTableCli", error)

    @staticmethod
    def selectCustomer():
        """

        Modulo para seleccionar un cliente y cargarlo en el formulario

        """
        try:
            row = globals.ui.tblCustomerList.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneCustomer(str(data[2]))
            boxes = [globals.ui.txtDniCif, globals.ui.txtDateCli, globals.ui.txtSurnameCli, globals.ui.txtNameCli,
                     globals.ui.txtEmailCli, globals.ui.txtMobileCli, globals.ui.txtAddressCli]

            for i in range(len(boxes)):
                boxes[i].setText(str(record[i]))

            globals.ui.cmbProvinceCli.setCurrentText(record[7])
            globals.ui.cmbCityCli.setCurrentText(record[8])
            if str(record[9]) == 'paper':
                globals.ui.rdbFacturePaper.setChecked(True)
            else:
                globals.ui.rdbFactureOnline.setChecked(True)

            globals.status = str(record[10])
            globals.ui.txtDniCif.setEnabled(False)
            globals.ui.txtDniCif.setStyleSheet('background-color: rgb(255, 255, 197);')

        except Exception as error:
            print("error en selectCustomer", error)

    @staticmethod
    def delClient(self):
        """

        Modulo para eliminar a un cliente y marcarlo como historico
        :param self: None
        :type self: None
        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec():
                dni = globals.ui.txtDniCif.text()
                if Conexion.deleteCli(dni):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Client")
                else:
                    print("Algo ha ido mal")
                Customers.loadTableCli(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error. Contact with the administrator or try again later.")


        except Exception as error:
            print("error en delCustomer", error)

    @staticmethod
    def saveClient():
        """

        Modulo para guardar los datos en la bbdd

        """
        try:
            newCli = [globals.ui.txtDniCif.text(), globals.ui.txtDateCli.text(), globals.ui.txtSurnameCli.text(),
                      globals.ui.txtNameCli.text(), globals.ui.txtEmailCli.text(), globals.ui.txtMobileCli.text(),
                      globals.ui.txtAddressCli.text(), globals.ui.cmbProvinceCli.currentText(), globals.ui.cmbCityCli.currentText()]
            if globals.ui.rdbFacturePaper.isChecked():
                fact = "paper"
            else:
                fact = "electronic"
            newCli.append(fact)
            if Conexion.addClient(newCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client Added")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, DNI or mobile exists")

            varCli = True
            Customers.loadTableCli(varCli)

        except Exception as error:
            print("error saveClient", error)

    @staticmethod
    def modifyClient():
        """

        Modulo para guardar modificaciones de un cliente en la bbdd

        """
        try:
            print(globals.status)
            if globals.status == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client not activated. Do you want activate it?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec():
                    globals.status = str("True")
                else:
                    globals.status = str("False")
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify Data")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Are you sure modify data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                dni = globals.ui.txtDniCif.text()
                modifyCli = [globals.ui.txtDateCli.text(), globals.ui.txtSurnameCli.text(),
                          globals.ui.txtNameCli.text(), globals.ui.txtEmailCli.text(), globals.ui.txtMobileCli.text(),
                          globals.ui.txtAddressCli.text(), globals.ui.cmbProvinceCli.currentText(),
                          globals.ui.cmbCityCli.currentText(), globals.status]
                if globals.ui.rdbFacturePaper.isChecked():
                    fact = "paper"
                else:
                    fact = "electronic"
                modifyCli.append(fact)
                if Conexion.modifyClient(dni, modifyCli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client Modified")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                    if mbox.exec():
                        mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Error modifying data")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()

            else:
                mbox.hide()
        except Exception as error:
            print("error modifyClient", error)

    @staticmethod
    def HistoricalCli():
        """

        Modulo para cargar la tabla clientes si queremos historico o no

        """
        try:
            if globals.ui.chcHistorical.isChecked():
                var = False
            else:
                var = True
            Customers.loadTableCli(var)
        except Exception as error:
            print("error HistoricalCli", error)

    @staticmethod
    def searchClient():
        """

        Modulo para buscar un cliente por su dni y cargarlo en el formulario

        """
        try:
            dni = globals.ui.txtDniCif.text()
            record = Conexion.dataOneCustomer(str(dni))
            if record == Conexion.dataOneCustomer(str(dni)):
                if not record:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client not exists")
                    if mbox.exec():
                        mbox.hide()
                        Customers.reloadClient()
                else:
                    box = [globals.ui.txtDniCif, globals.ui.txtDateCli, globals.ui.txtSurnameCli,
                           globals.ui.txtNameCli,globals.ui.txtEmailCli, globals.ui.txtMobileCli,
                           globals.ui.txtAddressCli]
                    for i in range(len(box)):
                        box[i].setText(str(record[i]))
                    globals.ui.cmbProvinceCli.setCurrentText(record[7])
                    globals.ui.cmbCityCli.setCurrentText(record[8])
                    if str(record[9]) == 'paper':
                        globals.ui.rdbFacturePaper.setChecked(True)
                    else:
                        globals.ui.rdbFactureOnline.setChecked(True)
                    if str(record[10]) == "False":
                        globals.ui.lblWarning.setText("Historical Client")
                        globals.ui.lblWarning.setStyleSheet("background-color: rgb(255, 255, 200); color: red")
                    else:
                        globals.ui.lblWarning.setText("")
                        globals.ui.lblWarning.setStyleSheet("background-color: rgb(244, 246, 248);")

        except Exception as error:
            print("error searchClient", error)
