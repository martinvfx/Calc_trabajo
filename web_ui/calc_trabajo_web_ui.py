import logging, time, os
import justpy as jp

from operations.functions import tiempos as operations_tiempos
from operations.functions import night_working_hours as operations_nwh
from operations.functions import calcular_total as operations_ctotal
app =jp.app

logging.basicConfig(level=logging.WARN)

## Description of elements styles attributes.
bbox_style = 'm-2 p-2 h-132 text-xl border-2 background-gray-300 text-white'
inbox_style = "flex m-1 h-6  text-sm bg-gray-200 font-mono font-bold border-2 border-gray-200 rounded px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
boton_style = "p-4 font-bold text-black bg-gray-500 border-2 border-gray  hover:bg-blue-300 rounded"
message_classes = 'ml-4 p-2 text-lg text-white overflow-auto font-mono rounded-lg'
label_item_clas = inbox_style.rsplit('bg-')[0]  # resuse of inbox style classes
cell_style = 'flex-col p-2 flex-grow-0  flex-shrink-0'

head_div = jp.Div(classes='m-2 flex border border-gray-800 overflow-auto', delete_flag=False)
logolink = jp.A(a=head_div, href='http://vfx-sup.com', target='_blank') #
logo = jp.Img(a=logolink, src='http://vfx-sup.com/wp-content/uploads/2017/05/CucardaVFXsup_fdoNegro-e1495057122527.png', classes="m-2 box-border object-left object-contain h-10") #TO-DO agregar link y un about a la main page .
info_link_box = jp.Div(classes ='justify-end')
info_link = jp.A(a=info_link_box, text='Info adicional', href='http://vfx-sup.com', title='Información del autor y de uso', classes='text-gray-800 align-middle text-xs text-right font-style: italic justify-end px-8') # , target='_blank' invisible bg-gray-900 border-2 border-gray-700
title_to_show = jp.P( text="Calculador de jornadas de filmación", classes='m-4 text-xl font-bold text-white overflow-auto')
result_display = jp.Div( name='result_display',  classes='inline-block align-top font-bold text-align-right flex-row ') # 'flex-col m-2 flex-shrink-0 '
espacios = jp.Space(num=4)

## input elements
fee_inbox = jp.Input(name="fee_in", value=0, type='number', title='Indique el costo por jornada acordado en el convernio colectivo o en el contrato\nNo utilizar decimales ni fracciones!', placeholder='honorarios', tabindex=1, classes=inbox_style, delete_flag=False)
fee_label = jp.Label(text='Valor de la jornada regular =', classes=label_item_clas)
factor_mult_extras_inbox = jp.Input(type='number', title='porcentaje de incremento por hora extra.\nUsualmente es 50%' ,
                                    value=50, tabindex=2, classes=inbox_style, delete_flag=False)
factor_mult_extras_label = jp.Label(text='Porcentaje por hora extra =', classes=label_item_clas)
start_workday_label = jp.Label(text='Inicio del trabajo =', classes=label_item_clas)
end_workday_label = jp.Label(text='Final del trabajo =', classes=label_item_clas)
start_workday_inbox = jp.Input(name='start_work', type='datetime-local', title='Indicar cuando empezó el trabajo', tabindex=4, classes=inbox_style, delete_flag=False)
end_workday_inbox = jp.Input(name='end_work', type='datetime-local', title='Indicar cuando finalizó el trabajo', tabindex=5, classes=inbox_style, delete_flag=False) # TO-DO que el end no pueda ser anterior al start day.
hs_por_jornada_inbox = jp.Input(type='number', title='Indicar cuantas horas tenés que trabajar diarimente por contrato.\n'
                                                     'Usualmente en cine son 12hs y en TV son 10hs'
                                , value=12, tabindex=4, classes=inbox_style, delete_flag=False)
hs_por_jornada_label = jp.Label(text='Horas por jornada regular =', classes=label_item_clas)
night_check = jp.Input(name='noc_chk', type='checkbox', title='Activarlo si deseas calcular diferenciando las horas nocturnas de las horas regulares.', tabindex=5, classes=inbox_style, delete_flag=False)
night_hs_label = jp.Label(text='Contabilizar horario nocturno', title='Horario nocturno: de 21 a 06 hs (durante ese lapso se computa 1 hora por cada 50 minutos trabajados)', classes=label_item_clas)

## Output labes for user info.
info_area = jp.Div(classes='flex border-gray-900 border-2 px-2 text-xs invisible') #
trab_un_total_label = jp.Label(text='Trabajaste un total de: ', classes=label_item_clas)
son_extras_label = jp.Label(text='De las cuales, son extras: ', classes=label_item_clas)
cobrar_hs_extras_label = jp.Label(text='Cobrarías: ', classes=label_item_clas)
avalorde_label = jp.Label(text='A valor de: ', classes=label_item_clas)


def start_setup():
    # Called once on startup
    head_div.add(jp.Space(num=25), title_to_show, info_link_box)


## Helper functions for do comunications to the backend.

def change(self, msg):
    self.before = style_ini = self.__getattribute__('classes')
    # print(style_ini )
    self.set_class('text-white') #visible bg-gray text-lg
    # self.after = print('esto es after change')
    self.after = self.set_class(style_ini)

def dates_non_overlap(self, msg):
    # print('funcion overlap ')
    if end_workday_inbox.value < start_workday_inbox.value:
        logging.warning(f'\n{start_workday_inbox.value} la salida debe ser posterior a la entrada!! ')
        self.before = end_workday_inbox.set_class('text-red-500')
        end_workday_inbox.value = start_workday_inbox.value
        info_area.delete_components()
        info_area.text = 'ATENCIÓN: la fecha de salida debe ser posterior a la entrada!! '
        info_area.set_class('text-red-500')
    else:
        end_workday_inbox.set_classes(inbox_style)
        info_area.text = ""
        info_area.set_class('text-white')


async def result(self, msg):
    result_display.delete_components()
    dates_non_overlap(self, msg)
    jor = str(fee_inbox.value)
    factor_mult_extras = float((factor_mult_extras_inbox.value /100) +1)
    r = jp.P(text=operations_ctotal(jor, factor_mult_extras, operations_tiempos(start_workday_inbox.value, end_workday_inbox.value, hs_por_jornada_inbox.value, night_check.value)[2], hs_por_jornada_inbox.value))
    result.output = r.text
    result.val_hs_extras = operations_ctotal.__getattribute__("val_hs_extras")
    result.hs_ext_trabajadas = operations_ctotal.__getattribute__("hs_ext_trabajadas")
    result.ganancia_por_hs_extras = operations_ctotal.__getattribute__("ganancia_por_hs_extras")
    result_int_part = str(r.text).rsplit(".")[0]
    result_display_decimal_part = str(r.text).rsplit(".")[1]
    rd = jp.Div(a=result_display, classes='flex content-start')
    rd.add(jp.Div(text=result_int_part, classes='text-xl'), jp.P(text='.'), jp.Div(text=result_display_decimal_part, classes='text-ms'))
    info_area_fn(self, msg)
    await rd.update()

def info_area_fn(self, msg):
    self.before = info_area.delete_components()
    info_area.set_class('visible')
    t = operations_tiempos(start_workday_inbox.value, end_workday_inbox.value, hs_por_jornada_inbox.value, night_check.value)
    ## funtion to return text labes values.
    def textlabel(self, value):
        txtemp = self.text.rstrip('.0123456789')
        self.text = txtemp + value
        return self.text
    trab_un_total_label.text = textlabel(trab_un_total_label, str(round(t[2], 1)))
    cobrar_hs_extras_label.text  = textlabel(cobrar_hs_extras_label, str(round(result.__getattribute__('ganancia_por_hs_extras'), 2)))
    # cobrar_hs_extras_label.text = f"{cobrar_hs_extras_label.text.split(':')[0]}: ${cobrar_hs_extras_label.text.split(':')[1].lstrip(' ')} por hs extras"
    avalorde_label.text  = textlabel(avalorde_label, str(round(result.__getattribute__('val_hs_extras'), 2)))
    # avalorde_label.text = f"{avalorde_label.text.split(':')[0]}: ${avalorde_label.text.split(':')[1].lstrip(' ')} por hora extra"
    son_extras_label.text = textlabel(son_extras_label, str(round(result.__getattribute__('hs_ext_trabajadas'), 2)))
    info_area.add(trab_un_total_label, espacios, son_extras_label, espacios, cobrar_hs_extras_label, espacios, avalorde_label)


async def web_ui(self):
    wp = jp.WebPage()
    wp.title = 'Calcuador de jornada de Filmación'
    # wp.favicon = "http://vfx-sup.com/wp-content/uploads/2017/05/CucardaVFXsup-150x150.png"
    main_div = jp.Div(a=wp , classes='bg-black py-2 px-2')
    main_div.add(head_div)

    app_box = jp.Div(a=main_div, classes='flex-col text-white content-center m-2 flex-shrink-0 ')
    d1_organizer = jp.Div(a=app_box, classes='flex border-gray-900 border-2')
    labels_for_data = jp.Div(a=d1_organizer, classes='text-align-left '+cell_style)
    data_input_column = jp.Div(a=d1_organizer, classes=cell_style)
    labels_for_data.add(fee_label, factor_mult_extras_label, start_workday_label, end_workday_label, hs_por_jornada_label, night_hs_label)
    data_input_column.add(fee_inbox, factor_mult_extras_inbox, start_workday_inbox, end_workday_inbox, hs_por_jornada_inbox, night_check)

    pre_info_area = jp.Div(a=app_box, classes='py-2')

    result_box = jp.Div(a=app_box, text='Cobrarás en Total =  ', classes=' flex content-start') # w-100
    result_box.add(result_display)
    calc_bton =jp.Button(text='Calcular Total', name='Calcular Total', a=app_box, click=result, classes=boton_style) # TO-DO activar la funcionalidad del horario nocturno cuanod de checke.
    pre_info_area.add(info_area)

    end_workday_inbox.on('change', dates_non_overlap)
    fee_inbox.on('change', result)

    # calc_bton.on('before', info_area_fn)
    info_link.on('mouseover', change)

    return wp

# if __name__ == '__main__':
jp.justpy(web_ui,  websockets=False) # startup=start_setup)
