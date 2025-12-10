import os
import sqlite3

import globals

from PyQt6 import QtSql, QtWidgets

class Conexion:
    def db_conexion(self = None):
        """

        Establece conexión con la base de datos local ``bbdd.sqlite``.

        Comprueba que el archivo existe, valida que tenga tablas y finalmente abre la conexión.

        :return: ``True`` si la conexión fue exitosa, ``False`` en caso contrario.
        :rtype: bool

        """

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
        """

        Obtiene la lista de provincias registradas en la tabla ``provincias``.

        :return: Lista con nombres de provincias.
        :rtype: list[str]

        """

        listprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listprov.append(query.value(1))
        return listprov

    @staticmethod
    def listMuniProv(province):
        """

        Obtiene todos los municipios pertenecientes a una provincia.

        :param str province: Nombre de la provincia.
        :return: Lista de municipios.
        :rtype: list[str]

        """

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
        """

        Obtiene una lista de clientes.

        :param bool varCli: Si es ``True`` devuelve solo clientes en histórico.
        :return: Lista de filas completas de la tabla customers.
        :rtype: list[list]

        """

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
        """

        Obtiene los datos de un cliente buscándolo por móvil o DNI/NIE.

        :param str dato: Móvil o DNI/NIE.
        :return: Lista con los datos del cliente.
        :rtype: list

        """

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
        """

        Marca un cliente como no histórico (reactivado).

        :param str dni: DNI/NIE del cliente.
        :return: ``True`` si la operación fue exitosa.
        :rtype: bool

        """

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
        """

        Inserta un nuevo cliente.

        :param list newCli: Datos del cliente.
        :return: ``True`` si se insertó correctamente.
        :rtype: bool

        """

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
        """

        Modifica los datos de un cliente existente.

        :param str dni: DNI/NIE del cliente.
        :param list modifyCli: Nuevos valores de los campos.
        :return: ``True`` si la actualización fue exitosa.
        :rtype: bool

        """

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




    @staticmethod
    def listProducts():
        """

        Obtiene la lista completa de productos.

        :return: Lista de filas de productos.
        :rtype: list[list]

        """

        list = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM products")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)
        return list

    @staticmethod
    def dataOneProduct(dato):
        """

        Obtiene los datos de un producto por su código.

        :param str dato: Código del producto.
        :return: Lista con datos del producto.
        :rtype: list

        """

        try:
            list = []
            dato = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM products where Code = :dato")
            query.bindValue(":dato", dato)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            return list

        except Exception as error:
            print("error dataOneCustomer", error)

    @staticmethod
    def addProduct(newProduct):
        """

        Inserta un nuevo producto.

        :param list newProduct: Datos del producto.
        :return: ``True`` si se insertó correctamente.
        :rtype: bool

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO products"
                          " ( Name, Stock, Family, UnitPrice )"
                          " VALUES "
                          " ( :name, :stock, :family, :unitPrice)")

            query.bindValue(":name", str(newProduct[0]))
            query.bindValue(":stock", str(newProduct[1]))
            query.bindValue(":family", str(newProduct[2]))
            query.bindValue(":unitPrice", str(newProduct[3]))

            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error addProduct", error)

    @staticmethod
    def deleteProduct(code):
        """

        Elimina un producto por su código.

        :param int code: Código del producto.
        :return: ``True`` si se eliminó correctamente.
        :rtype: bool

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM products WHERE Code = :code")
            query.bindValue(":code", int(code))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error deleteProduct", error)

    def modifyProduct(id, modpro):
        """

        Modifica los datos de un producto existente.

        :param int id: Código del producto.
        :param list modpro: Nuevos valores.
        :return: ``True`` si se actualizó correctamente.
        :rtype: bool

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE products SET Name= :name, Family =:family, Stock = :stock, "
                          " UnitPrice =:unitPrice where Code = :code" )
            query.bindValue(":code", int(id))
            query.bindValue(":name", str(modpro[0]))
            query.bindValue(":family", str(modpro[1]))
            query.bindValue(":stock", int(modpro[2]))
            price = modpro[3].replace("€", "")
            query.bindValue(":unitPrice", str(price))
            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error modifyPro", error)



    @staticmethod
    def searchClient(dni):
        """

        Verifica si existe un cliente por DNI.

        :param str dni: DNI/NIE.
        :return: ``True`` si existe.
        :rtype: bool

        """

        try:
            dni = str(dni).upper()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False

        except Exception as error:
            print("error searchClient", error)

    @staticmethod
    def insertInvoice(dni, data):
        """

        Inserta una factura.

        :param str dni: DNI del cliente.
        :param str data: Fecha de la factura.
        :return: ``True`` si se insertó correctamente.
        :rtype: bool

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dninie, data) values (:dni, :data)")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(data))
            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error insertInvoice", error)

    @staticmethod
    def allInvoices():
        """

        Obtiene todas las facturas ordenadas por ID descendente.

        :return: Lista de facturas.
        :rtype: list[list[str]]

        """

        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices ORDER BY idfact DESC")
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)
            return records

        except Exception as error:
            print("error allInvoices", error)

    @staticmethod
    def dataOneInvoice(idfact):
        """

        Obtiene los datos de una factura por ID.

        :param int idfact: ID de la factura.
        :return: Lista con datos de la factura.
        :rtype: list

        """

        try:
            list = []
            idfact = str(idfact).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices WHERE idfact = :idfact")
            query.bindValue(":idfact", idfact)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            return list

        except Exception as error:
            print("error dataOneInvoice", error)

    @staticmethod
    def dataOneSale(idfac):
        """

        Obtiene las líneas de venta de una factura.

        :param int idfac: ID de la factura.
        :return: Lista con líneas de venta.
        :rtype: list[list]

        """

        try:
            rows = []
            idfac = str(idfac).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idfac = :idfac")
            query.bindValue(":idfac", idfac)

            if query.exec():
                while query.next():
                    row = [query.value(2), query.value(4), query.value(5), query.value(3), query.value(6)]
                    rows.append(row)
            return rows

        except Exception as error:
            print("error dataOneInvoice", error)

    @staticmethod
    def selectProduct(item):
        """

        Obtiene el nombre y precio de un producto.

        :param int item: Código del producto.
        :return: Lista con nombre y precio.
        :rtype: list[str]

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT Name, UnitPrice FROM products WHERE Code = :code")
            query.bindValue(":code", int(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
            return row

        except Exception as error:
            print("error selectProduct", error)

    @staticmethod
    def saveSales(data):
        """

        Inserta una línea de venta asociada a una factura.

        :param list data: Datos de la venta (idfac, idpro, product, unitprice, amount, total)
        :return: ``True`` si se insertó correctamente.
        :rtype: bool

        """

        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales (idfac, idpro, product, unitprice, amount, total) "
                          " VALUES (:idfac, :idpro, :product, :unitprice, :amount, :total)")
            query.bindValue(":idfac", data[0])
            query.bindValue(":idpro", data[1])
            query.bindValue(":product", data[2])
            query.bindValue(":unitprice", data[3])
            query.bindValue(":amount", data[4])
            query.bindValue(":total", data[5])
            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error saveSales conexion", error)