import csv
import os
import sys
import time
import conexion
import customers
import events
import globals
import shutil
from datetime import datetime
#from venAux import About
import zipfile
from window import *


class Events:

    @staticmethod
    def messageExit(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            mbox.setWindowTitle("Exit")
            mbox.setText("Are you sure you want to exit?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Si")
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText("No")
            mbox.resize(600, 800)  # No funciona si no usa QDialog porque QmessageBox lo tiene bloqueado
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("Error en salida", e)

    @staticmethod
    def openAbout():
        try:
            globals.about.show()
        except Exception as e:
            print("Error al abrir About:", e)

    @staticmethod
    def closeAbout(self=None):
        try:
            globals.about.hide()
        except Exception as e:
            print("Error al cerrar About:", e)

    @staticmethod
    def openCalendar():
        try:
            globals.vencal.show()

        except Exception as e:
            print("Error en calendario", e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.panelMain.currentIndex() == 0:
                globals.ui.txtDateCli.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    def loadProv(self):
        try:
            globals.ui.cmbProvinceCli.clear()
            list = conexion.Conexion.listProv(self)
            globals.ui.cmbProvinceCli.addItems(list)
        except Exception as e:
            print("error load province", e)

    @staticmethod
    def loadMuni():
        try:
            province = globals.ui.cmbProvinceCli.currentText()
            list = conexion.Conexion.listMuniProv(province)
            globals.ui.cmbCityCli.clear()
            globals.ui.cmbCityCli.addItems(list)
        except Exception as e:
            print("error load cities", e)

    def resizeTabCustomer(self):
        try:
            header = globals.ui.tblCustomerList.horizontalHeader()
            for i in range(header.count()):
                if i == 7:
                    header.setSelectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tblCustomerList.horizontalHeaderItem(i)
                # negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clients: ", e)

    @staticmethod
    def saveBackup():
        try:
            data = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            filename = str(data) + "_backup.zip"
            directory, file = globals.dlgOpen.getSaveFileName(None, "Save Backup File", filename, 'zip')
            if globals.dlgOpen.accept and file:
                print(directory)
                filezip = zipfile.ZipFile(file, 'w')
                filezip.write('./data/bbdd.sqlite', os.path.basename('bbdd.sqlite'), zipfile.ZIP_DEFLATED)
                filezip.close()
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle("Save Backup")
                mbox.setText("Save Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error saveBackup", e)

    def restoreBackup(self):
        try:
            filename = globals.dlgOpen.getOpenFileName(None, "Restore Backup File", '', '*.zip;;ALl Files (*)')
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd='./data')
                    shutil.move('bbdd.sqlite', './data')
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle("Restore Backup")
                mbox.setText("Restore Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                conexion.Conexion.db_conexion(self)
                Events.loadProv(self)
                customers.Customers.loadTableCli(self)
        except Exception as e:
            print("error restoreBackup: ", e)

    def exportXlsCustomers(self):
        try:
            data = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            filename = str(data) + "_customers.csv"
            directory, file = globals.dlgOpen.getSaveFileName(None, "Save Backup File", filename, '.csv')
            var = False
            if file:
                records = conexion.Conexion.listCustomers(var)
                with open(file, "w", newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow('DNI_NIE', 'Adddata', 'Surname', 'Name', 'eMail', 'Mobile', 'Address',
                                     'Province', 'City', 'InvoiceType', 'Active')
                    for record in records:
                        writer.writerow(record)
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Export Customers Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Export Customers Error")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error esportXlsCustomers", e)

    def loadStatusBar(self):
        try:
            data = datetime.now().strftime('%d/%m/%Y')
            self.labelstatus = QtWidgets.QLabel(self)
            self.labelstatus.setText("Date: " + data + " - Version 0.0.1")
            self.labelstatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelstatus.setStyleSheet("color: white; font-weight: bold; font-size: 9px;")
            globals.ui.statusbar.addPermanentWidget(self.labelstatus, 1)
        except Exception as e:
            print("error loadStatusBar: ", e)
