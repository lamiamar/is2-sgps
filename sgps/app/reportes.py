from geraldo import Report, landscape, ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label

from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm
       
class ReporteUsuarios(Report):
    title = 'Reporte de Usuarios'

    page_size = landscape(A5)
    margin_left = 1*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
   
    class band_begin(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='', top=0.1*cm,
                left=8*cm),
        ]

    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='id', top=0, left=0.5*cm),
            ObjectValue(attribute_name='username', top=0, left=2.5*cm),
            ObjectValue(attribute_name='first_name', top=0, left=4.5*cm),
            ObjectValue(attribute_name='last_name', top=0, left=6.5*cm),
            ObjectValue(attribute_name='email', top=0, left=8.5*cm),
            )
       
    class band_page_header(ReportBand):
        height = 1.2*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="ID", top=0.8*cm, left=0.5*cm),
            Label(text=u"Usuario", top=0.8*cm, left=2.5*cm),
            Label(text=u"Nombre", top=0.8*cm, left=4.5*cm),
            Label(text=u"Apellido", top=0.8*cm, left=6.5*cm),
            Label(text=u"Email", top=0.8*cm, left=8.5*cm),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}       
       
class ReporteProyectos(Report):
    title = 'Reporte de Proyectos'

    page_size = landscape(A5)
    margin_left = 1*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
   
    class band_begin(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='', top=0.1*cm,
                left=8*cm),
        ]

    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='id', top=0, left=0.5*cm),
            ObjectValue(attribute_name='Usuario', top=0, left=2.5*cm),
            ObjectValue(attribute_name='Nombre', top=0, left=4.5*cm),
            ObjectValue(attribute_name='Fecha', top=0, left=6*cm),
            ObjectValue(attribute_name='Descripcion', top=0, left=12*cm),
            )
       
    class band_page_header(ReportBand):
        height = 1.2*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="ID", top=0.8*cm, left=0.5*cm),
            Label(text=u"Lide del Proyecto", top=0.8*cm, left=2.5*cm),
            Label(text=u"Nombre", top=0.8*cm, left=4.5*cm),
            Label(text=u"Fecha de Creacion", top=0.8*cm, left=6*cm),
            Label(text=u"Descripcion", top=0.8*cm, left=12*cm),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reportes de SGPS', top=0.1*cm),
            SystemField(expression=u'%(now:%Y, %b %d)s  %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}

class ReporteRoles(Report):
    title = 'Reporte de Roles'

    page_size = landscape(A5)
    margin_left = 1*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
   
    class band_begin(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='', top=0.1*cm,
                left=8*cm),
        ]

    class band_detail(ReportBand):
        height = 1*cm
        elements=(
            ObjectValue(attribute_name='id', top=0, left=0.5*cm),
            ObjectValue(attribute_name='Nombre', top=0, left=1.5*cm),
            ObjectValue(attribute_name='Tipo', top=0, left=5*cm),
            ObjectValue(attribute_name='Descripcion', top=0, left=6.5*cm),
            )
       
    class band_page_header(ReportBand):
        height = 1.2*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="ID", top=0.8*cm, left=0.5*cm),
            Label(text=u"Nombre", top=0.8*cm, left=1.5*cm),
            Label(text=u"Tipo", top=0.8*cm, left=4.5*cm),
            Label(text=u"Descripcion", top=0.8*cm, left=6.5*cm),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}
       
       
class ReporteArtefactos(Report):
    title = 'Reporte de Artefactos'

    page_size = landscape(A5)
    margin_left = 1*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
   
    class band_begin(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='', top=0.1*cm,
                left=8*cm),
        ]

    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='id', top=0, left=0.5*cm),
            ObjectValue(attribute_name='Nombre', top=0, left=2*cm),
            ObjectValue(attribute_name='DescripcionCorta', top=0, left=3*cm),
            ObjectValue(attribute_name='DescripcionLarga', top=0, left=6*cm),
            ObjectValue(attribute_name='Proyecto', top=0, left=8*cm),
            ObjectValue(attribute_name='Complejidad', top=0, left=10*cm),
            ObjectValue(attribute_name='Prioridad', top=0, left=11*cm),
            ObjectValue(attribute_name='Version', top=0, left=12*cm),
            ObjectValue(attribute_name='Usuario', top=0, left=14*cm),
            
            )
       
    class band_page_header(ReportBand):
        height = 1.2*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="ID", top=0.8*cm, left=0.5*cm),
            Label(text=u"Nombre", top=0.8*cm, left=2*cm),
            Label(text=u"Descripcion_Corta", top=0.8*cm, left=4*cm),
            Label(text=u"Descripcion_Larga", top=0.8*cm, left=6*cm),
            Label(text=u"Proyecto", top=0.8*cm, left=9*cm),
            Label(text=u"Complejidad", top=0.8*cm, left=11*cm),
            Label(text=u"Prioridad", top=0.8*cm, left=12*cm),
            Label(text=u"Version", top=0.8*cm, left=13*cm),
            Label(text=u"Usuario", top=0.8*cm, left=14*cm),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reportes deSGPS', top=0.1*cm),
            SystemField(expression=u'Printed in %(now:%Y, %b %d)s at %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}       
       
       
class ReporteHistoriales(Report):
    title = 'Reporte de Historial'

    page_size = landscape(A5)
    margin_left = 1*cm
    margin_top = 1*cm
    margin_right = 1*cm
    margin_bottom = 1*cm
   
    class band_begin(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='', top=0.1*cm,
                left=8*cm),
        ]


    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='id', top=0, left=0.5*cm),
            ObjectValue(attribute_name='Nombre', top=0, left=1.5*cm),
            ObjectValue(attribute_name='DescripcionCorta', top=0, left=3.5*cm),
            ObjectValue(attribute_name='DescripcionLarga', top=0, left=6*cm),
            ObjectValue(attribute_name='Prioridad', top=0, left=7*cm),
            ObjectValue(attribute_name='Version', top=0, left=8*cm),
            ObjectValue(attribute_name='Complejidad', top=0, left=9*cm),
            ObjectValue(attribute_name='Fecha_mod', top=0, left=12*cm),
            )
       
    class band_page_header(ReportBand):
        height = 1.2*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="ID", top=0.8*cm, left=0.5*cm),
            Label(text=u"Nombre", top=0.8*cm, left=1.5*cm),
            Label(text=u"DescripcionCorta", top=0.8*cm, left=3*cm),
            Label(text=u"DescripcionLarga", top=0.8*cm, left=6*cm),
            Label(text=u"Prioridad", top=0.8*cm, left=7*cm),
            Label(text=u"Version", top=0.8*cm, left=8*cm),
            Label(text=u"Complejidad", top=0.8*cm, left=9*cm),
            Label(text=u"Fecha de Modificacion", top=0.8*cm, left=11*cm),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Reportes de SGPS', top=0.1*cm),
            SystemField(expression=u'Printed in %(now:%Y, %b %d)s at %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}
