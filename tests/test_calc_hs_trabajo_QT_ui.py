import unittest, sys, logging
from PySide2 import QtTest

import calc_hs_trabajo as cht
from PySide2 import QtCore, QtGui, QtWidgets
dt = QtCore.QDateTime

app = QtWidgets.QApplication(sys.argv)

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    def setUp(self):
       self.win = cht.principal()

    # test input journal value an just calc hitting enter.
    def test_input_journal_value(self):
        # parameters for test
        self.win.dia_hora_entrada.setDateTime(QtCore.QDateTime(2010,10,1, 0,0,0))
        self.win.dia_hora_salida.setDateTime(QtCore.QDateTime(2010,10,1, 18,0,0))
        self.win.valorjornada_LEd.setText("55")     ## I put an arbritrary journal rate.

        # Push Calcular Total button with the left mouse button
        Calc_hit = self.win.calcular_pbt
        QtTest.QTest.mouseClick(Calc_hit, QtCore.Qt.LeftButton)

        self.assertEqual(self.win.valorjornada_LEd.text(), "55")
        self.assertEqual(self.win.TotalaCobrar_LCD.value(), 96.25)

    # test with nigth hours checked on.
    def test_with_night_checked_on(self):
        # parameters for test
        self.win.dia_hora_entrada.setDateTime(QtCore.QDateTime(2010,10,1, 0,0,0))
        self.win.dia_hora_salida.setDateTime(QtCore.QDateTime(2010,10,1, 18,0,0))
        self.win.valorjornada_LEd.setText("55")     ## I put an arbritrary journal rate.
        self.win.hnocturno_checkbox.setChecked(True)

        # hit Calcular Total button with the left mouse button
        Calc_hit = self.win.calcular_pbt
        QtTest.QTest.mouseClick(Calc_hit, QtCore.Qt.LeftButton)

        # self.assertEqual(self.win.valorjornada_LEd.text(), "55")
        self.assertEqual(round(self.win.TotalaCobrar_LCD.value(), 2), 104.5) #

## 24hs con horario nocturno chequeado es 149.8 $

if __name__ == '__main__':
    unittest.main()
