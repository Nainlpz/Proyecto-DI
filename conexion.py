import os
import sqlite3
import globals

from PyQt6 import QtSql, QtWidgets

class Conexion:
    def db_conexion(self = None):
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self=None):

        listprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listprov.append(query.value(1))
        return listprov

    @staticmethod
    def listMuniProv(province):
        try:
            listmunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listmunicipios.append(query.value(1))
            return listmunicipios
        except Exception as e:
            print("error load cities", e)

    @staticmethod
    def listCustomers(varCli):
        list = []
        if varCli:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where historical = :true order by surname")
            query.bindValue(":true", str(True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range (query.record().count())]
                    list.append(row)
        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers order by surname")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range (query.record().count())]
                    list.append(row)
        return list

    @staticmethod
    def dataOneCustomer(dato):
        try:
            list = []
            dato = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where mobile = :dato")
            query.bindValue(":dato", str(dato))
            if query.exec():
                while query.next():
                    for i in range (query.record().count()):
                        list.append(query.value(i))
            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers where dni_nie = :dato")
                query.bindValue(":dato", str(dato))
                if query.exec():
                    while query.next():
                        for i in range (query.record().count()):
                            list.append(query.value(i))
            return list
        except Exception as error:
            print("error dataOneCustomer", error)

    @staticmethod
    def deleteCli(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set historical = :value WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":value", str(False))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error deleteCli", error)

    @staticmethod
    def addClient(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers"
                          " ( dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical )"
                          " VALUES "
                          " ( :dni_nie, :adddata, :surname, :name, :mail, :mobile, :address, :province, :city, :invoicetype, :historical)")
            query.bindValue(":dni_nie", str(newCli[0]))
            query.bindValue(":adddata", str(newCli[1]))
            query.bindValue(":surname", str(newCli[2]))
            query.bindValue(":name", str(newCli[3]))
            query.bindValue(":mail", str(newCli[4]))
            query.bindValue(":mobile", str(newCli[5]))
            query.bindValue(":address", str(newCli[6]))
            query.bindValue(":province", str(newCli[7]))
            query.bindValue(":city", str(newCli[8]))
            query.bindValue(":invoicetype", str(newCli[9]))
            query.bindValue(":historical", str(True))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error addClient", error)

    @staticmethod
    def modifyClient(dni, modifyCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET adddata = :adddata, surname = :surname, name = :name, mail = :mail,"
                          " mobile = :mobile, address = :address, province = :province, city = :city,"
                          " invoicetype = :invoicetype, historical = :historical"
                          " WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":adddata", str(modifyCli[0]))
            query.bindValue(":surname", str(modifyCli[1]))
            query.bindValue(":name", str(modifyCli[2]))
            query.bindValue(":mail", str(modifyCli[3]))
            query.bindValue(":mobile", str(modifyCli[4]))
            query.bindValue(":address", str(modifyCli[5]))
            query.bindValue(":province", str(modifyCli[6]))
            query.bindValue(":city", str(modifyCli[7]))
            query.bindValue(":historical", str(modifyCli[8]))
            query.bindValue(":invoicetype", str(modifyCli[9]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error modifyClient", error)

