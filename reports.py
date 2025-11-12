from tkinter import Image

from reportlab.pdfgen import canvas
import os, datetime
from conexion import *
from PIL import Image

class Reports():

    def __init__(self):
        rootPath = ".\\reports"
        data = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        self.namereportcli = data + "_reportcustomers.pdf"
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath

    def footer(self, title):
        try:
            self.c.line(35, 65, 525, 65)
            day = datetime.datetime.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            self.c.setFont('Helvetica', 7)
            self.c.drawString(40, 50, day)
            self.c.drawString(260, 50, title)
            self.c.drawString(500, 50, 'Page ' + str(self.c.getPageNumber()))
        except Exception as e:
            print("error en footer", e)

    def top(self, title):
        try:
            path_logo = r".\img\logo.ico"
            logo = Image.open(path_logo)
            if isinstance(logo, Image.Image):
                self.c.line(45, 770, 175, 770)
                self.c.line(45, 705, 175, 705)
                self.c.line(45, 770, 45, 705)
                self.c.line(175, 770, 175, 705)
                self.c.setFont('Helvetica-Bold', 10)
                self.c.drawString(55, 785, "EMPRESA TEIS")
                self.c.drawCentredString(300, 675, title)
                self.c.line(35, 665, 525, 665)
                self.c.drawImage(path_logo, 490, 765, width=40, height=40)
                self.c.setFont("Helvetica", 9)
                self.c.drawString(55, 755, 'CIF: A12345678')
                self.c.drawString(55, 745, 'Avenida de Galicia, 101')
                self.c.drawString(55, 735, 'Vigo - 36215 - España')
                self.c.drawString(55, 725, 'Tlfo: 986 123 456')
                self.c.drawString(55, 715, 'teis@mail.com')
            else:
                print("error cargar imagen")
        except Exception as e:
            print("error top", e)

    def reportCustomers(self):
        try:
            title = "Customers List"
            self.footer(title)
            self.top(title)
            var = False
            records = Conexion.listCustomers(var)
            items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(40, 650, str(items[0]))
            self.c.drawString(100, 650, str(items[1]))
            self.c.drawString(180, 650, str(items[2]))
            self.c.drawString(260, 650, str(items[3]))
            self.c.drawString(330, 650, str(items[4]))
            self.c.drawString(390, 650, str(items[5]))
            self.c.drawString(480, 650, str(items[6]))
            self.c.line(35, 645, 525, 645)
            y = 630
            for record in records:
                if y <= 90:
                    self.c.setFont("Helvetica-Oblique", 8)
                    self.c.drawString(480, 75, "Next Page")
                    self.c.showPage() # Crea nueva página
                    self.footer(title)
                    self.top(title)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    self.c.setFont("Helvetica-Bold", 10)
                    self.c.drawString(40, 650, str(items[0]))
                    self.c.drawString(100, 650, str(items[1]))
                    self.c.drawString(180, 650, str(items[2]))
                    self.c.drawString(260, 650, str(items[3]))
                    self.c.drawString(330, 650, str(items[4]))
                    self.c.drawString(390, 650, str(items[5]))
                    self.c.drawString(480, 650, str(items[6]))
                    self.c.line(35, 645, 525, 645)
                    y = 630
                self.c.setFont("Helvetica", 8)
                dni = '*****' + str(record[0][5:9])
                self.c.drawString(40, y, dni)
                self.c.drawString(100, y, str(record[2]))
                self.c.drawString(180, y, str(record[3]))
                self.c.drawString(260, y, str(record[5]))
                self.c.drawString(330, y, str(record[8]))
                self.c.drawString(410, y, str(record[9]))
                if str(record[10]) == 'True':
                    self.c.drawString(490, y, "Alta")
                else:
                    self.c.drawString(490, y, "Baja")
                y = y - 25
            self.c.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)

        except Exception as e:
            print("error en reportCustomers", e)