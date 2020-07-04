import unittest, sys, logging
# sys.path.append("horario_N/horario_nocturno_scratch_1")
sys.path.insert(1, 'C:/Users\Tato\PycharmProjects\Test_General\pyside_Learning\QT_aprendiendo')

# from horario_N import horario_nocturno_scratch_1
from QT_aprendiendo.calc_hs_trabajo import principal
from QT_aprendiendo.calc_hs_trabajo import tiempos, night_working_hours
from PySide2 import QtCore, QtGui, QtWidgets
dt = QtCore.QDateTime

import numpy as np

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.entrada = "00:00"
        self.salida = "05:00"

    # pruebo horario de madrugada de 00 a 05hs
    def test_horario_nocturno_madrugada(self):
        entrada = "2020-01-01T00:00"
        salida = "2020-01-01T05:00"
        hnocturno_checkbox = True
        # capture_results
        r_fueron_las_horas, r_total_hs_nocturnas, r_hs_trabajadas_totales = principal.night_working_hours(self, entrada, salida, hnocturno_checkbox)

        self.assertEqual( r_total_hs_nocturnas, 5)  # expected 5
        self.assertEqual( r_hs_trabajadas_totales, 5)   # expected 5

    # pruebo horario de noche de 21 a 23hs
    def test_horario_nocturno_noche(self):
        # seteo nuevos horarios
        entrada = "2020-01-01T21:00"
        salida = "2020-01-01T23:00"
        hnocturno_checkbox = True

        # capture_results
        r_fueron_las_horas, r_total_hs_nocturnas, r_hs_trabajadas_totales = principal.night_working_hours(self, entrada, salida, hnocturno_checkbox) # , date_entrada=self.date_entrada, date_salida=self.date_salida

        # self.assertEqual( r_fueron_las_horas , True)
        self.assertEqual( r_total_hs_nocturnas, 2)  # expected 2
        self.assertEqual( r_hs_trabajadas_totales, 2)    # expected 2

    def test_horario_nocturno_noche_pasanto_standartimeISO(self):
        # seteo nuevos horarios
        entrada = "2020-01-10T21:00"
        salida = "2020-01-10T23:00"
        hnocturno_checkbox = True

        # capture_results
        r_fueron_las_horas, r_total_hs_nocturnas, r_hs_trabajadas_totales = principal.night_working_hours(self,entrada, salida, hnocturno_checkbox) # , date_entrada=date_entrada, date_salida=date_salida

        # self.assertEqual( r_fueron_las_horas , True)
        self.assertEqual( r_total_hs_nocturnas, 2)  # expected 2
        self.assertEqual( r_hs_trabajadas_totales, 2)    # expected 2

    #  pruebo horario de noche de 04 a 23hs misma jornada.
    def test_horario_nocturno_madrugada_y_noche(self):
        # seteo nuevos horarios
        entrada = "2020-01-01T04:00"
        salida = "2020-01-01T23:00"
        hnocturno_checkbox = True

        # capture_results
        r_fueron_las_horas, r_total_hs_nocturnas, r_hs_trabajadas_totales = principal.night_working_hours(self, entrada, salida, hnocturno_checkbox)

        # self.assertEqual( r_fueron_las_horas , True)
        self.assertEqual( r_total_hs_nocturnas, 3.98)  # expected 3.98
        self.assertEqual( r_hs_trabajadas_totales, 19)    # expected 19


    #  pruebo jornada superlarga de 01 día1 a 03 hs del otro día.
    def test_horario_nocturno_pasando_de_jornada_medianoche(self):
        logging.info('\n'*2+'\t'*3+'--- pruebo jornada superlarga de 01 hs día1 a 03 hs pasando de fecha.')
        # parametros a testear
        entrada = "2020-01-01T23:00"
        salida = "2020-01-02T03:00"
        hnocturno_checkbox = True

        # capture_results
        r_fueron_las_horas, r_total_hs_nocturnas, r_hs_trabajadas_totales = principal.night_working_hours(self, entrada, salida, hnocturno_checkbox)

        # self.assertEqual( r_fueron_las_horas , True)
        self.assertEqual( r_total_hs_nocturnas, 3.98)  # expected 3.98
        self.assertEqual( r_hs_trabajadas_totales, 4)    # expected 4

        # print(r_fueron_las_horas)


    #  pruebo funcion tiempos.
    def test_tiempos_function(self):
        # parametros a testear
        entrada = "2020-01-01T00:00"
        salida = "2020-01-01T08:00"
        hs_por_jornada = 12
        hnocturno_checkbox = False

        # capture_results
        minutos_tiempo_transcurrido_totaljornada, bloque_de_12hs, r_horas_trasncurridas = tiempos(entrada, salida, hs_por_jornada, hnocturno_checkbox)  # , night_working_hours(self, entrada, salida, hnocturno_checkbox)

        # self.assertEqual( r_fueron_las_horas , True)
        self.assertEqual(r_horas_trasncurridas, 8)  # expected 8

if __name__ == '__main__':
    unittest.main()
