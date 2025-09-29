import re

import globals

class Customers:
    @staticmethod
    def checkDni(self=None):
        try:
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
                    globals.ui.txtDniCif.setFocus()
            else:
                globals.ui.txtDniCif.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDniCif.setText(None)
                globals.ui.txtDniCif.setFocus()
        except Exception as error:
            print("error en validar dni ", error)

    def capLetter(text, widget):
        try:
            text = text.title()
            widget.setText(text)
        except Exception as error:
            print("error al capitalizar texto ", error)

    def checkEmail(email):
        regex = r'[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(regex, email):
            globals.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtEmailCli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtEmailCli.setText(None)
            globals.ui.txtEmailCli.setPlaceholderText("Invalid Email")
            globals.ui.txtEmailCli.setFocus()

    def checkMobile(number):
        regex = r'^[67]\d{8}$'
        if re.match(regex, number):
            globals.ui.txtMobileCli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobileCli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobileCli.setText(None)
            globals.ui.txtMobileCli.setPlaceholderText("Invalid Mobile")
            globals.ui.txtMobileCli.setFocus()