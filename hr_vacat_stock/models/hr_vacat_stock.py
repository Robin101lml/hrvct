# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _,tools
from dateutil.relativedelta import relativedelta
from datetime import date
import time

#diseñado para mostrar el inventario de vacaciones de los empleados /Solo días pendientes actualmente

class HrEmployeeVacatStock(models.Model):
    _name = 'hr.vacat.stock'
    _description = 'HR Employee vacaciones'

    employee_ref = fields.Many2one('hr.employee',string="empleado", copy=False,store=True)
    cantidad_dias = fields.Float(string="Días",store=True)
    cantidad_horas = fields.Float(string="Horas",store=True)
    cantidad_minutos = fields.Float(string="Minutos",store=True)
    desc=fields.Text(string="Comentarios")
    permisos = fields.Many2one('hr.leave', string="Permisos", copy=False, store=True)
    vacaciones = fields.Many2one('hr.vacat.form', string="Vacaciones", copy=False, store=True)



    def action_post(self,):
        self.write({'cantidad_minutos': '0.00'})

    def generar_bolsa_vacaciones(self):
        #        Ejecutar el 1 de cada mes para actualizar la fecha de vacaciones de empleadoa antiguos
        #consultar los contratos activos, fecha de inicio y los empleados //////////////////////////////////////////////////////////////////////////////////
        try:
            consulta= """SELECT ct.id as contrato_id, ct.company_id, ct.employee_id,hr.name,hr.tipo_dias_vacaciones, ct.state, ct.date_start, ct.date_end, ct.fecha_ultimas_vacaciones
                                  FROM hr_contract  as ct  JOIN hr_employee as hr ON ct.employee_id = hr.id 
                                  WHERE ct.active = TRUE AND hr.active =TRUE AND ct.state = 'open' and ct.date_end is null  """

            self._cr.execute(consulta)
            data =""
            data = self._cr.fetchall()
            data = list(data)
            filas=len(data)
            if filas>0: #verificar que existan empleados con contratos activos
                for a in data:
                    contrato=a[0]
                    #empresas=a[1]
                    empleado_id=a[2]
                    #empleado_nombre=a[3]
                    tipo_dias_vacaciones=a[4]
                    #estado_contrato=a[5]
                    fecha_inicio=a[6]
                    #fecha_fin=a[7]
                    fecha_ultimasVac=a[8]

                    if (fecha_ultimasVac):  # Verifica si es un empleado antiguo
                        resultadobl = self.funcVerifMes(fecha_ultimasVac, tipo_dias_vacaciones, 1)
                        if (resultadobl):
                            if (tipo_dias_vacaciones == "t30"):
                                cantidad_dias = 30
                            else:
                                cantidad_dias = 26
                            vacaciones = {
                                'employee_ref': empleado_id,
                                'cantidad_dias': cantidad_dias,
                                'cantidad_horas':0.00,
                                'cantidad_minutos':0.00,
                                'desc': 'bolsa de vaciones correspondiente al mes de: %s' % (str(datetime.now().strftime("/%b/%Y")))
                                }
                            bolsa=self.env['hr.vacat.stock'].create(vacaciones)
                            bolsa.action_post()
                            # actualizar fecha de utlimas vacaciones del empleado en el contrato.
                            other_model_record = self.env['hr.contract'].search([('id', '=', contrato)], limit=1)
                            other_model_record.write({'fecha_ultimas_vacaciones': datetime.now()})
                    else: # es empelado nuevo menos de 1 año de servicio
                        resultadobl = self.funcVerifMes(fecha_inicio, tipo_dias_vacaciones, 2)
                        if (resultadobl):
                            if (tipo_dias_vacaciones == "t30"):
                                cantidad_dias = 30
                            else:
                                cantidad_dias = 26
                            vacaciones = {
                                'employee_ref': empleado_id,
                                'cantidad_dias': cantidad_dias,
                                'cantidad_horas': 0.00,
                                'cantidad_minutos': 0.00,
                                'desc': 'bolsa de vaciones correspondiente al mes de: %s' % (str(datetime.now().strftime("/%b/%Y")))
                            }
                            bolsa = self.env['hr.vacat.stock'].create(vacaciones)
                            bolsa.action_post()
                            #actualizar fecha de utlimas vacaciones del empleado en el contrato.
                            other_model_record = self.env['hr.contract'].search([('id', '=', contrato)], limit=1)
                            other_model_record.write({'fecha_ultimas_vacaciones': datetime.now()})
        except Exception:
            realizado=False
            #enviar mensaje a alguien de algún error en la ejecución


# funciónpara validar fecha del contrato y calcular la difrenica con respecto a la fecha actual
    def funcDateDiference(self,fecha_inicio):
        if str(fecha_inicio) <= str(datetime.now()):
            antig = relativedelta(datetime.now(),
                                  datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day))
            return antig
        else:
            return False

# Función para validar cantidad de años, meses y días
    def funcVerifMes(self,fecha, tipo_dias_vacaciones, tipo):
        if (self.funcDateDiference(fecha)):
            antig = self.funcDateDiference(fecha)
            antiguedad_anos = antig.years
            antiguedad_mese = antig.months
            antiguedad_dias = antig.days
            #print("Años: %s, Meses:  %s, Días: %s" % (str(antig.years), str(antig.months), str(antig.days)))
            if (tipo == 1):
                if (antiguedad_anos == 1):
                    #si es empleado antiguo y tiene un año desde sus últimas vacacioens aplica, de lo contrario no
                    return True
                else:
                    return False
            else:
                if (antiguedad_mese > 10 and antiguedad_mese <= 11) or (antiguedad_mese == 10 and antiguedad_dias > 16):
                    # si tiene entre 10 y 11 meses calicifa, si tiene 10 meses con mas de 16 días califica
                    # de lo contrario caerá en el siguiente mes
                    # esto se utiliza para normalizar al empleado y asignarle un mes de vacaciones el 12 a partir del inicio
                    return True  # crear bolsa de vacaciones
                else:
                    if(antiguedad_anos>=1):
                        return True
                    else:
                        return False

        else:
            return "no cumple", False


#informe tipo lista de los empelados y el día que corresponde cada uno
# solo los empleados activos y que tengan contratos vigentes "open"
class HrEmployeeVacatStockconsult(models.Model):
    """Se consulta sumando cuantos días tiene cada persona"""
    _name = "hr.vacat.stock.view"
    _auto = False
    _order = "dias desc"

    name = fields.Many2one('hr.employee',string="empleado", copy=False)
    company = fields.Many2one('res.company',string="Empresa", copy=False)
    dias = fields.Float(string="Días", default=0)
    horas = fields.Float(string="Horas" , default=0)
    minutos = fields.Float(string="Minutos" , default=0 )

    def _select(self):
        select_str = """
                min(hr.id) as id, hr.id as name , sum(COALESCE(hvs.cantidad_dias,0)) as dias, sum(COALESCE(hvs.cantidad_horas,0)) as horas,
                 sum(COALESCE(hvs.cantidad_minutos,0)) as minutos ,cmp.id as company """
        return select_str

    def _from(self):
        from_str = """
                  hr_employee as hr 
					LEFT JOIN hr_vacat_stock as hvs on hvs.employee_ref=hr.id
                    INNER JOIN res_company as cmp on hr.company_id = cmp.id
					INNER JOIN hr_contract as ct on hr.id = ct.employee_id
                """
        return from_str


    def _group_by(self):
        group_by_str = """ WHERE 	hr.active='True' and ct.state='open'
                           GROUP BY hr.id, hvs.employee_ref,cmp.id,ct.employee_id
					       ORDER BY dias DESC NULLS LAST """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as ( select
                           %s
                           FROM %s
                           %s
                           )""" % (self._table, self._select(), self._from(), self._group_by()))



#extención para crear un registro al aprobarse un permiso de tipo contra vacaciones código=CVAC
# genera un negativo que reta al inventario
class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'
    def action_validate(self):
        res = super(HolidaysRequest, self).action_validate()

        for em in self:
            if self.holiday_status_id.code=="CVAC":
                if(self.number_of_days>0.00):
                    horas=0
                else:
                    horas=self.number_of_hours_display*-1

                if(self.name):
                    desc="Permiso "+str(self.holiday_status_id.name)+" "+str(self.name)
                else:
                    desc="Permiso "+str(self.holiday_status_id.name) + " "

                permiso = self.env['hr.vacat.stock'].create({
                    'employee_ref': self.employee_id.id,
                    'cantidad_dias': self.number_of_days *-1,
                    'cantidad_horas': horas,
                    'cantidad_minutos': 0.00,
                    'desc': desc,
                    'permisos': self.id,

                })
                permiso.action_post()

        return res

#extención para añadir una fecha en la de se generaron la última bolsa de vacaciones basadas en contratos por empleados

class HrContract(models.Model):
    """
        fecha de últimas vacaciones
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    fecha_ultimas_vacaciones = fields.Date(string="Fecha de ultimas vacaciones", store=True)

