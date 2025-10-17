import sys
import time
import conexion
import globals
#from venAux import About
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
    def messageAbout(self=None):
        try:
            globals.about.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
            globals.about.setWindowTitle("About")
            globals.about.exec()
        except Exception as e:
            print("Error al abrir About:", e)

    @staticmethod
    def openAbout():
        try:
            globals.about.show()
        except Exception as e:
            print("Error al abrir About:", e)

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
                if i == 6:
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
