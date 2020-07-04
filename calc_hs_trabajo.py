import sys, os, logging, datetime
import numpy as np
from ui.calcHsExtras_ui import *

from operations.functions import tiempos as operations_tiempos
from operations.functions import night_working_hours as operations_nwh
from operations.functions import calcular_total as operations_ctotal
# TO-DO cambiar de las funciones locales a las funciones importadas desde .operations.functios.

logging.basicConfig(level=logging.DEBUG)

factor_h_nocturna = 1.2 # 20% es el equivalente a la hora de 50min.

class principal(QtWidgets.QMainWindow, Ui_CalcMainWindow):
    def __init__(self):
        super(principal, self).__init__()
        self.setupUi(self)

        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()

        # ppmsg = popup_message()
        # ppmsg.warning('please enter a value in pesos as number') # TO-FIX

        ## set days of default dates:
        Qdate = QtCore.QDateTime
        self.dia_hora_entrada.setDateTime(Qdate.currentDateTime())
        self.dia_hora_salida.setDateTime(Qdate.addDays(Qdate.currentDateTime(), 1))
        self.dia_hora_entrada.dateTimeChanged.connect(lambda :self.dia_hora_salida.setMinimumDateTime(self.dia_hora_entrada.dateTime()))
        # self.dia_hora_entrada.dateChanged.connect(lambda :self.dia_hora_salida.setDateTime(self.dia_hora_entrada.dateTime()))
        self.dia_hs_entrada_str =  self.dia_hora_entrada.dateTime().toString("yyyy-MM-ddTHH:mm")  ## Lo convierto a string time standar ISO 8601 para pasarlo a la funcion tiempos.
        self.dia_hora_salida_str =  self.dia_hora_salida.dateTime().toString("yyyy-MM-ddTHH:mm")  ## Lo convierto a string time standar ISO 8601 para pasarlo a la funcion tiempos.

        ## Actions:
        self.hnocturno_checkbox_state = self.hnocturno_checkbox.isChecked()
        self.nwh = night_working_hours(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hnocturno_checkbox_state)
        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()     ## to get the spinbox value al every time it change.
        # calling to the final calc function
        calc_lambda = lambda: calcular_total(self.valorjornada_LEd.text(), float((self.porcentaje_hs_extras_spinBox.value() /100) +1), tiempos(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hs_por_jornada, self.hnocturno_checkbox_state)[2], self.hs_por_jornada)
        self.valorjornada_LEd.setFocus()
        self.valorjornada_LEd.setCursorPosition(0)
        self.hnocturno_checkbox.toggled.connect(calc_lambda)  # TO-DO TO-FIX no esta andando porque no cambia el resultado cuando se activa el checkbox
        self.calcular_pbt.clicked.connect(lambda: self.TotalaCobrar_LCD.display(calcular_total(self.valorjornada_LEd.text(), float((self.porcentaje_hs_extras_spinBox.value() /100) +1), tiempos(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hs_por_jornada, self.hnocturno_checkbox)[2], self.hs_por_jornada)))
        self.calcular_pbt.clicked.connect(lambda: self.output_labels_reaction())
        self.valorjornada_LEd.returnPressed.connect(calc_lambda)
        self.valorjornada_LEd.returnPressed.connect(lambda: self.output_labels_reaction())
        self.duracion_Jornada_spinBox.valueChanged[int].connect(lambda: self.duracion_Jornada_spinBox.value())     ## to get the spinbox value al every time it change.

    def output_labels_reaction(self):
        ## this is not a class-method , it's just a function to group label setters.
        self.horas_trasncurridas = tiempos(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hs_por_jornada, self.hnocturno_checkbox)[2]
        # print(' \n !!!mensaje: variable horas_trasncurridas es = %s \n' % (self.horas_trasncurridas))
        self.horasTrabajadas_label.setText(str(round(self.horas_trasncurridas) if ".0" in str(self.horas_trasncurridas) else str(round(self.horas_trasncurridas, 2))))

        calcular_total(self.valorjornada_LEd.text(), float((self.porcentaje_hs_extras_spinBox.value() /100) +1), tiempos(self.dia_hs_entrada_str, self.dia_hora_salida_str, self.hs_por_jornada, self.hnocturno_checkbox_state)[2], self.hs_por_jornada)

        self.gananciaHsExtra_label.setText(str(round(calcular_total.ganancia_por_hs_extras, 2)) if calcular_total.ganancia_por_hs_extras >= 0 else 0)
        # # show amount of extra hours
        self.son_hs_extras_label.setText(str(round(calcular_total.hs_ext_trabajadas) if ".0" in str(calcular_total.hs_ext_trabajadas) else str(round(calcular_total.hs_ext_trabajadas, 2))))
        # # show unit value per extra hour.
        self.valor_x_hsextra_label.setText(str(round(calcular_total.val_hs_extras, 2)))

    def cambio_hs_x_jornada_spinbox(self):
        self.valJornada_L.setText("Honoraios por jornada regular de %s hs" % (self.duracion_Jornada_spinBox.value()))
        logging.info('\n'+"ha cambiado el spinbox a %s" % (self.duracion_Jornada_spinBox.value()))
        self.hs_por_jornada = self.duracion_Jornada_spinBox.value()  ## to get the spinbox value al every time it change.
        # self.calcular_total(self.valorjornada_LEd.text())

        self.duracion_Jornada_spinBox.valueChanged[int].connect(lambda: cambio_hs_x_jornada_spinbox())
        self.porcentaje_hs_extras_spinBox.valueChanged[int].connect(lambda: calcular_total(self.valorjornada_LEd.text()) )


def night_working_hours(entrada, salida, hnocturno_checkbox): # date_entrada, date_salida,  # , **kwargs
    # I will assign two range of hours that is taken as "night time range"
    io_madrugada = [i.split(":") for i in ["00:00", "05:59"]]
    io_nocturno = [i.split(":") for i in ["21:00", "23:59"]]

    # ========= convirtiendo entrada ==========
    # ent  = entrada.split('T')[1]
    # sali = salida.split('T')[1]
    date_entrada = entrada.split('T')[0]
    # date_salida = salida.split('T')[0]

    ent = np.datetime64(entrada)
    sal = np.datetime64(salida)

    # logging.debug("\n entrada es = %s \n salida es = %s" % (ent, sal))

    total_worked_hs = float(str(((sal - ent) / 60)).replace("minutes", 'horas').rstrip(" horas"))
    tiempo_trabajado = np.arange(ent, sal, dtype='datetime64[m]')

    horario_madrugada = np.arange(('%sT%s:%s' % (date_entrada, io_madrugada[0][0], io_madrugada[0][1])), ('%sT%s:%s' % (date_entrada, io_madrugada[1][0], io_madrugada[1][1])), dtype='datetime64[m]') # TO-DO revisar acá cuando cambie date_entrada en ambas puntas.
    horario_nocturno = np.arange(('%sT%s:%s' % (date_entrada, io_nocturno[0][0], io_nocturno[0][1])), ('%sT%s:%s' % (date_entrada, io_nocturno[1][0], io_nocturno[1][1])), dtype='datetime64[m]') # TO-DO revisar acá cuando cambie date_entrada en ambas puntas de la expresion.
    horarios_combinados = np.concatenate((horario_madrugada, horario_nocturno), axis=0)
    logging.info(f'el horario nocturno empieza a las {horario_madrugada[0]} y termina a las {horario_nocturno[-1]}')
    h_trabajadas_nocturnas = np.in1d(tiempo_trabajado, horarios_combinados)
    h_trabajadas_de_noche = np.in1d(tiempo_trabajado, horario_nocturno)

    rango_horas_nocturnas = [str(t.tolist().time()) for t in horarios_combinados]
    rango_horas_trabajado = [str(t.tolist().time()) for t in tiempo_trabajado]
    minutes_worked_en_nocturno_list = [t for t in rango_horas_trabajado if t in rango_horas_nocturnas]
    total_night_worked_hs_asdecimal = 0 # just for initialize this variable.

    if hnocturno_checkbox == True:
        if len(minutes_worked_en_nocturno_list) > 0:
            # hs_worked_at_night_list = ( tiempo_trabajado[h_trabajadas_de_noche]).astype('M8[h]')
            total_night_worked_hs_asdecimal = (len(minutes_worked_en_nocturno_list) / 60).__round__(2)

            logging.info("si está!\n%s \nfueron las horas en las que trabajaste entre 21 y 6am"
                         "\nUn total de= %s horas nocturnas (en decimal)"
                         "\nsobre %s horas Totales trabajadas" % (
                         (str(minutes_worked_en_nocturno_list[0]) + '\t' + str(minutes_worked_en_nocturno_list[-1])), total_night_worked_hs_asdecimal, total_worked_hs))
        logging.info("\ntotal worked hs = %s " % (total_worked_hs))
    else:
        total_night_worked_hs_asdecimal = 0
    return minutes_worked_en_nocturno_list, total_night_worked_hs_asdecimal, total_worked_hs

def tiempos(dia_hora_entrada, dia_hora_salida, hs_por_jornada, hnocturno_checkbox):  # , night_working_hours # TO-FIX no está calculando bien las horas trabajadas ni extras.
    dia_hora_entrada = datetime.datetime.strptime(dia_hora_entrada, '%Y-%m-%dT%H:%M') ## ahora es un objeto datetime.
    dia_hora_salida = datetime.datetime.strptime(dia_hora_salida, '%Y-%m-%dT%H:%M') ## ahora es un objeto datetime.

    minutos_tiempo_transcurrido_totaljornada = (dia_hora_salida - dia_hora_entrada).total_seconds() / 60
    # print(minutos_tiempo_transcurrido_totaljornada)
    horas_trasncurridas = minutos_tiempo_transcurrido_totaljornada / 60
    if horas_trasncurridas >= hs_por_jornada:
        bloque_de_12hs = (horas_trasncurridas / hs_por_jornada)
    else:
        bloque_de_12hs = 1

    logging.info('\n'+"Es una jornada mayor a %s" % hs_por_jornada) if horas_trasncurridas >= hs_por_jornada else None
    logging.info('\n'+"trasncurrió entre las dos fechas = %s minutos, que son unas %s horas" % (
        minutos_tiempo_transcurrido_totaljornada, horas_trasncurridas))

    # Horario nocturno: de 21 a 06 hs (durante ese lapso se computa 1 hora por cada 50 minutos trabajados)
    if hnocturno_checkbox == True:
        nwhs = night_working_hours(dia_hora_entrada.strftime("%Y-%m-%dT%H:%M"), dia_hora_salida.strftime("%Y-%m-%dT%H:%M"), hnocturno_checkbox) #  night_working_hours(horaminuto_entrada, horaminuto_salida, hnocturno_checkbox)
        # horas_trasncurridas = horas_trasncurridas + (self.night_working_hours(horaminuto_entrada, horaminuto_salida)[1] * 1.2) # 20% es el equivalente a la hora de 50min.
        nwhs_decimal = nwhs[1]
        horas_trasncurridas = horas_trasncurridas - nwhs_decimal + (nwhs_decimal * factor_h_nocturna ) # 20% es el equivalente a la hora de 50min.
        logging.debug('---- horas transcurridas calculando nocturnas == %s '
                      '\t------  horas transcurridas sin contar noct == %s ' % (horas_trasncurridas, (minutos_tiempo_transcurrido_totaljornada/60)))

    return minutos_tiempo_transcurrido_totaljornada, bloque_de_12hs, horas_trasncurridas


## calculador final de totales a mostrar.
def calcular_total( jor, factor_mult_extras, horas_trasncurridas, hs_por_jornada):
    if jor is None:
        jor = "0.0"
    jor = float(jor.replace(",", ".") if "," in jor else jor)

    valor_hora = jor / hs_por_jornada
    calcular_total.hs_ext_trabajadas = 0 if horas_trasncurridas <= hs_por_jornada else horas_trasncurridas - hs_por_jornada    # es el total de horas transcurridas en el trabajo, restandoles las horas incluidas en la jornada regular.
    calcular_total.val_hs_extras = valor_hora * factor_mult_extras if factor_mult_extras >= 0 else valor_hora
    calcular_total.ganancia_por_hs_extras = calcular_total.val_hs_extras * calcular_total.hs_ext_trabajadas    # How much you ern for extras = cost for hour multiply for charge factor multiply worked hours minus hours of regular work day. .

    paga = round((((calcular_total.hs_ext_trabajadas ) * factor_mult_extras) * valor_hora) + jor, 2)
    logging.debug('\n ==================>> \n'
          '%s = hs extras totales contemplando nocturnas \n'
          '%s = Hs nocturnas contadas x factor hs nocturnas' % (round((calcular_total.hs_ext_trabajadas),2)," ver nwhs_decimal"))
    return paga

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


