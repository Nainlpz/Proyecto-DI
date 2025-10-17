import events
import globals
from calendar import *
from about import *
from datetime import datetime

class Calendar (QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        globals.vencal.Calendar.setSelectedDate((QtCore.QDate(year, month, day)))
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)


class About (QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        self.ui.btnCloseAbout.clicked.connect(events.Events.messageAbout)


