import sys, numpy
import datetime
sys.path.insert(1, 'C:/Users\Tato\PycharmProjects\Test_General\pyside_Learning\QT_aprendiendo')
import unittest
from QT_aprendiendo.calc_hs_trabajo import calcular_total
from PySide2 import QtCore, QtGui, QtWidgets
dt = QtCore.QDateTime

import pyside_Learning.QT_aprendiendo.calc_hs_trabajo as cht

class Test_functions(unittest.TestCase):
    # test calc function only with 12hs for regular working day, and 24hs of worked time.
    def test_calcular_total_function_12x24(self):
        # test parameters
        jor = str(55)
        factor_mult_extras = 1.5
        horas_trasncurridas = 24
        hs_por_jornada = 12

        # capture output test
        paga = cht.calcular_total(jor, factor_mult_extras, horas_trasncurridas, hs_por_jornada)
        self.assertEqual(paga , 137.5) # total of pay result

    def test_tiempos_function(self):
        # test parameters
        dia_hora_entrada_dt ='2020-06-10T22:00' # datetime.datetime.strptime('2020-06-10T22:00', '%Y-%m-%dT%H:%M')
        dia_hora_salida_dt = '2020-06-11T22:00' # datetime.datetime.strptime('2020-06-11T22:00', '%Y-%m-%dT%H:%M')
        hs_por_jornada = 12
        hnocturno_checkbox = False
        night_working_hours = 12.0

        # capture output test
        horas_transcurridas = cht.tiempos(dia_hora_entrada_dt, dia_hora_salida_dt, hs_por_jornada, hnocturno_checkbox)[2]
        self.assertEqual(horas_transcurridas, 24) # total hours elapsed

if __name__ == '__main__':
    unittest.main()
