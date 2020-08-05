import sys, os, logging, datetime
import numpy as np
from ui.calcHsExtras_ui import *

from operations.functions import tiempos as op_tiempos
from operations.functions import night_working_hours as op_nwh
from operations.functions import calcular_total as op_ctotal

logging.basicConfig(level=logging.DEBUG)

factor_h_nocturna = 1.2 # 20% es el equivalente a la hora de 50min.

class principal(QtWidgets.QMainWindow, Ui_CalcMainWindow):
    def __init__(self):
        super(principal, self).__init__()
        self.setupUi(self)

        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()

        ## set days of default dates:
        Qdate = QtCore.QDateTime
        self.dia_hora_entrada.setDateTime(Qdate.currentDateTime())
        self.dia_hora_salida.setDateTime(Qdate.addDays(Qdate.currentDateTime(), 1))
        self.dia_hora_entrada.dateTimeChanged.connect(lambda :self.dia_hora_salida.setMinimumDateTime(self.dia_hora_entrada.dateTime()))
        ## accion que cambia las variables fechas cuando los inbox cambian.
        self.dia_hora_entrada.dateTimeChanged.connect(lambda : self.on_dates_change())
        self.dia_hora_salida.dateTimeChanged.connect(lambda : self.on_dates_change())
        self.dia_hs_entrada_str , self.dia_hora_salida_str = self.on_dates_change()

        ## Actions:
        self.nwh = op_nwh(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hnocturno_checkbox_state)
        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()     ## to get the spinbox value al every time is changed.
        ## calling to the final calc function
        calc_lambda = lambda: op_ctotal(self.valorjornada_LEd.text(), float((self.porcentaje_hs_extras_spinBox.value() /100) +1), r_tiempos, self.hs_por_jornada)
        self.valorjornada_LEd.setFocus()
        self.valorjornada_LEd.setCursorPosition(0)
        self.hnocturno_checkbox.stateChanged.connect( lambda :self.on_dates_change() and calc_lambda and self.output_labels_reaction())
        self.calcular_pbt.clicked.connect(lambda: self.output_labels_reaction())
        self.valorjornada_LEd.returnPressed.connect(calc_lambda)
        self.valorjornada_LEd.returnPressed.connect(lambda: self.output_labels_reaction())
        self.duracion_Jornada_spinBox.valueChanged[int].connect(lambda: self.duracion_Jornada_spinBox.value())     ## to get the spinbox value al every time it change.


    def on_dates_change(self):
        self.hnocturno_checkbox_state = True if self.hnocturno_checkbox.isChecked() else False
        self.dia_hs_entrada_str =  self.dia_hora_entrada.dateTime().toString("yyyy-MM-ddTHH:mm")  ## Lo convierto a string time standar ISO 8601 para pasarlo a la funcion op_tiempos.
        self.dia_hora_salida_str =  self.dia_hora_salida.dateTime().toString("yyyy-MM-ddTHH:mm")  ## Lo convierto a string time standar ISO 8601 para pasarlo a la funcion op_tiempos.
        global r_tiempos
        r_tiempos =  op_tiempos(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hs_por_jornada, self.hnocturno_checkbox_state)[2]

        return self.dia_hs_entrada_str , self.dia_hora_salida_str

    def output_labels_reaction(self):
        ## this is not a class-method , it's just a function to group label setters.
        if not self.valorjornada_LEd.text().isnumeric():
            ppmsg = QtWidgets.QMessageBox.information(self, 'Atencion', 'Debes ingresar un número por jornada\n para poder hacer el calculo',)
            self.valorjornada_LEd.setFocus()

        # # refresh final result display
        self.TotalaCobrar_LCD.display(op_ctotal(self.valorjornada_LEd.text(), float((self.porcentaje_hs_extras_spinBox.value() /100) +1), r_tiempos, self.hs_por_jornada))
        self.horas_trasncurridas = r_tiempos
        self.horasTrabajadas_label.setText(str(round(self.horas_trasncurridas) if ".0" in str(self.horas_trasncurridas) else str(round(self.horas_trasncurridas, 2))))

        self.gananciaHsExtra_label.setText(str(round(op_ctotal.ganancia_por_hs_extras, 2)) if op_ctotal.ganancia_por_hs_extras >= 0 else 0)
        # # show amount of extra hours
        self.son_hs_extras_label.setText(str(round(op_ctotal.hs_ext_trabajadas) if ".0" in str(op_ctotal.hs_ext_trabajadas) else str(round(op_ctotal.hs_ext_trabajadas, 2))))
        # # show unit value per extra hour.
        self.valor_x_hsextra_label.setText(str(round(op_ctotal.val_hs_extras, 2)))

    def cambio_hs_x_jornada_spinbox(self):
        self.valJornada_L.setText("Honoraios por jornada regular de %s hs" % (self.duracion_Jornada_spinBox.value()))
        logging.info('\n'+"ha cambiado el spinbox a %s" % (self.duracion_Jornada_spinBox.value()))
        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()  ## to get the spinbox value al every time it change.
        # self.op_ctotal(self.valorjornada_LEd.text())

        # self.duracion_Jornada_spinBox.valueChanged[int].connect(lambda: cambio_hs_x_jornada_spinbox())
        self.porcentaje_hs_extras_spinBox.valueChanged[int].connect(lambda: op_ctotal(self.valorjornada_LEd.text()) )





class Popup_message(QtWidgets.QMessageBox):
    def __init__(self, msg):
        self.msg = msg
        # self.about('Error', 'please enter a value in pesos as number')
        self.about('Error', msg)
        logging.warning(msg)


if __name__ == '__main__':
    curr_path = os.path.dirname(__file__)
    ui_path = "ui/"
    ui_file = "calcHsExtras.ui"
    ui_file_path = os.path.normpath(os.path.join(os.path.join(curr_path, os.path.dirname(ui_path)),
                                                 ui_file))

    app = QtWidgets.QApplication(sys.argv)
    application = principal()
    application.show()
    sys.exit(app.exec_())


