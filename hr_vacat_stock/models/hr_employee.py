from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta

#muestra las nominas que se le han pagado al empleado anteriormente
#en la aplicación de empleados
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'


    #consulta mediante funciones computadas la cnatidad de días horas, minutos disponibles en el inventario de tiempo

    cantidad_dias = fields.Integer(string=_("Días"), compute='_compute_vacat_stock')
    cantidad_horas = fields.Integer(string=_("Horas"), compute='_compute_vacat_stock')
    cantidad_minutos = fields.Integer(string=_("Minutos"), compute='_compute_vacat_stock')
    #definido por tipos de empleados nortmal t30, casos especiales t26
    tipo_dias_vacaciones=fields.Selection(selection=[
                                                    ("t26", "Tipo 26"),
                                                    ("t30", "Tipo 30"),
                                                ],
                                                    string="Tipo vacaciones 26/30",  default='t30', readonly=False, copy=False, tracking=True, store=True, required=True)




    def _compute_vacat_stock(self):
        for employee in self:
            aux = 0
            aux2 = 0
            aux3 = 0
            document_ids = self.env['hr.vacat.stock'].search([('employee_ref', '=', employee.id)])
            if document_ids:
                for a in document_ids:
                    aux = aux + a.cantidad_dias
                    aux2 =aux2 + a.cantidad_horas
                    aux3 = aux3 + a.cantidad_minutos

            employee.cantidad_dias = int(aux) #len(employee.employee_vaccination_ids)
            employee.cantidad_horas = int(aux2)
            employee.cantidad_minutos = int(aux3)


    def inventario_tiempo(self):#llama una vista de tipo tree con el detalle de cada suma o resta en el inventario de ese empleado
        self.ensure_one()
        domain = [
            ('employee_ref', '=', self.id)]
        return {
            'name': _('Inventario_tiempo'),
            'domain': domain,
            'res_model': 'hr.vacat.stock',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                                   Click para crear nuevos registros
                                </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref':%s}" % self.id
        }


    #Datos Complementarios solicitados por recursos humanos
    direccion_completa=fields.Text(string="Dirección",store=True,)
    corregimiento=fields.Char(string="Corregimiento", )
    distrito=fields.Char(string="Distrito", )
    provincia=fields.Char(string="Provincia", )
    telefono=fields.Char(string="Teléfono", )
    correopersonal=fields.Char(string="Correo Personal",store=True,)
    edad=fields.Char(string="Edad", compute="_get_edad", store=True)#computar con la fecha de nacimiento

    @api.depends("birthday")
    def _get_edad(self):
        for a in self:
            if (a.birthday):
                birthDate = a.birthday
                today = date.today()
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                a.edad = str(age)+" Años"  # Calcular edad
            else:
                a.edad = "0 Años"

    enfermedad=fields.Char(string="Sufre de alguna enfermedad?")

    personas_vive=fields.One2many("hr.empl.person.live","payslip_run_id",string="Personas con quien vive", store=True, index=True)
    persoans_depende=fields.One2many("hr.empl.person.depend","payslip_run_id",string="Personas que dependen",store=True, index=True)
    #anexar estos docuemntos
    cedula=fields.Boolean(string="Cédula")
    cedfecha=fields.Date(string="Fecha")
    hoja_vida=fields.Boolean(string="Hoja de vida")
    hoja_vida_fecha=fields.Date(string="Fecha")
    recordp=fields.Boolean(string="Record Policivo")
    recordpfecha=fields.Date(string="Fecha")
    titulo=fields.Boolean(string="Títulación ")
    titulofecha=fields.Date(string="Fecha")
    cartas_ref=fields.Boolean(string="Cartas de Referencia laboral")
    cartas_reffecha=fields.Date(string="Fecha")


#En caso de error en los la aplicación de permisos verificar y habilitar las variables siguientes


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"
    _description = 'Employee public'
    cantidad_dias = fields.Integer(string=_("Días"), compute='_compute_vacat_stock')
    cantidad_horas = fields.Integer(string=_("Horas"), compute='_compute_vacat_stock')
    cantidad_minutos = fields.Integer(string=_("Minutos"), compute='_compute_vacat_stock')
    tipo_dias_vacaciones=fields.Selection(selection=[
                                                    ("t26", "Tipo 26"),
                                                    ("t30", "Tipo 30"),
                                                ],
                                                    string="Tipo 26/30",  default='t30', readonly=False, copy=False, tracking=True, store=True, )

    def _compute_vacat_stock(self):
        for employee in self:
            aux = 0
            aux2 = 0
            aux3 = 0

            document_ids = self.env['hr.vacat.stock'].search([('employee_ref', '=', employee.id)])
            if document_ids:
                for a in document_ids:
                    aux = aux + a.cantidad_dias
                    aux2 = aux2 + a.cantidad_horas
                    aux3 = aux3 + a.cantidad_minutos

            employee.cantidad_dias = aux  # len(employee.employee_vaccination_ids)
            employee.cantidad_horas = aux2
            employee.cantidad_minutos = aux3


    def inventario_tiempo(self):#llama una vista de tipo tree con el detalle de cada suma o resta en el inventario de ese empleado
        self.ensure_one()
        domain = [
            ('employee_ref', '=', self.id)]
        return {
            'name': _('Inventario_tiempo'),
            'domain': domain,
            'res_model': 'hr.vacat.stock',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                                   Click para crear nuevos registros
                                </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref':%s}" % self.id
        }

    # Datos Complementarios
    direccion_completa = fields.Text(string="Dirección", store=True, )
    corregimiento = fields.Char(string="Corregimiento", )
    distrito = fields.Char(string="Distrito", )
    provincia = fields.Char(string="Provincia", )
    telefono = fields.Char(string="Teléfono", )
    correopersonal = fields.Char(string="Correo Personal", store=True, )
    edad = fields.Char(string="Edad",   store=True)  # computar con la fecha de nacimiento

    #no se calcula la edad ya que birthday no eziste en la tabla de he.employee.public

    enfermedad = fields.Char(string="Sufre de alguna enfermedad?")

    personas_vive = fields.One2many("hr.empl.person.live", "payslip_run_id", string="Personas con quien vive",
                                    store=True, index=True)
    persoans_depende = fields.One2many("hr.empl.person.depend", "payslip_run_id", string="Personas que dependen",
                                       store=True, index=True)
    # anexar estos docuemntos
    cedula = fields.Boolean(string="Cédula")
    cedfecha = fields.Date(string="Fecha")
    hoja_vida = fields.Boolean(string="Hoja de vida")
    hoja_vida_fecha = fields.Date(string="Fecha")
    recordp = fields.Boolean(string="Record Policivo")
    recordpfecha = fields.Date(string="Fecha")
    titulo = fields.Boolean(string="Títulación ")
    titulofecha = fields.Date(string="Fecha")
    cartas_ref = fields.Boolean(string="Cartas de Referencia laboral")
    cartas_reffecha = fields.Date(string="Fecha")


# se extiende para mostrar mediante campos relacionados el inventario a los empleados

class User(models.Model):
    _inherit = ['res.users']

    cantidad_dias = fields.Integer(related='employee_id.cantidad_dias', string="Días" )
    cantidad_horas = fields.Integer(related='employee_id.cantidad_horas', string="Horas" )
    cantidad_minutos = fields.Integer(related='employee_id.cantidad_minutos', string="Minutos" )

    def inventario_tiempo(self):#llama una vista de tipo tree con el detalle de cada suma o resta en el inventario de ese empleado
        self.ensure_one()
