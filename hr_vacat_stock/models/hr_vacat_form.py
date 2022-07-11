# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _,tools
from dateutil.relativedelta import relativedelta
from datetime import date
import time

# diseñado para crear formulario de vacaciones del empleado para firma e impresión y rebajar del invetario

class HrEmployeeVacatForm(models.Model):
    _name = 'hr.vacat.form'
    _description = 'Formulario de Vacaciones'
    _inherit = [ 'mail.thread', 'mail.activity.mixin']

    name=fields.Char(String="name", compute="_get_name",store=True,)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Aprobado'),
        ('cancel', 'Cancelado'),

    ], string='Status', store=True, tracking=True, copy=False, default="draft", readonly=False,
        help="")
    employee_id = fields.Many2one('hr.employee',string="EMPLEADO", copy=False,store=True,
                                  readonly=True, states={'draft': [('readonly', False)]},)
    company_id = fields.Many2one(related='employee_id.company_id', string="EMPRESA",store=True,)
    fecha_inicio = fields.Date(string="Fecha de Inicio",
                               readonly=True, states={'draft': [('readonly', False)]},store=True,)
    fecha_fin = fields.Date(string="Fecha fin",
                                    readonly=True, states={'draft': [('readonly', False)]},store=True,)
    request_hour_from = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '12:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], default="8",string='Hora de inicio',store=True,)
    request_hour_to = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '12:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], default="17.5",string='Hoora fin')
    dias = fields.Integer(string="Días",compute="_get_cantidad_dias")
    razon=fields.Text(string="Razón",  default="Vacaciones Correspondientes...",
                      readonly=True, states={'draft': [('readonly', False)]}, store=True,)

    contrato=fields.Many2one('hr.contract', string="Contrato", #default=lambda self: self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)],  limit=1),
                             readonly=True, states={'draft': [('readonly', False)]}, store=True,)

    @api.depends('employee_id','fecha_inicio')
    def _get_name(self):
        for a in self:
            if a.employee_id and a.fecha_fin:
                a.name="Vacaciones disfrutadas %s, (%s)"%(str(a.employee_id.name),str(a.fecha_inicio))
            else:
                a.name=""
    @api.depends('fecha_inicio','fecha_fin')
    def _get_cantidad_dias(self):
        for a in self:
            if (a.fecha_inicio and a.fecha_fin)and (str(a.fecha_fin)>str(a.fecha_inicio)):
                antig = relativedelta(datetime(a.fecha_fin.year, a.fecha_fin.month, a.fecha_fin.day),
                                      datetime(a.fecha_inicio.year, a.fecha_inicio.month, a.fecha_inicio.day))
                a.dias=antig.days+1
            else:
                a.dias =0


    def aprobar_vacaciones(self):
        self.write({
            'state': 'confirm',})
        # crear registro en el inventario para rebajar días
        permiso = self.env['hr.vacat.stock'].create({
            'employee_ref': self.employee_id.id,
            'cantidad_dias': self.dias * -1,
            'cantidad_horas': 0.00,
            'cantidad_minutos': 0.00,
            'desc': self.razon,
            'vacaciones': self.id,
        })
        permiso.action_post()
        return True
    def cancelar_vacaciones(self):
        self.write({
            'state': 'cancel',})
        return True
    def borrador_vacaciones(self):
        self.write({
            'state': 'draft',})
        return True