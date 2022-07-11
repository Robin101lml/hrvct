# -*- coding: utf-8 -*-

#Formulario tablas adicionales para añadir información de los empleados
#personas con las que vive y depende para complementar el contrato

from datetime import datetime, date, timedelta
from odoo import models, fields, api, _


class HrEmployeePersonLive(models.Model):
    _name = 'hr.empl.person.live'
    _description = 'HR Employee Personas con quien vive'
    _rac_name = "nombre_aplellido"
    payslip_run_id = fields.Many2one('hr.employee', string='empelado', readonly=True,
                                     copy=False,store=True)
    nombre_aplellido=fields.Char(string="Nombre y apellido",store=True)
    parentesco=fields.Char(string="Parentesco",store=True)
    cedula=fields.Char(string="cédula",store=True)
    fecha_nac=fields.Date(string="Fecha de Nacimiento",store=True)
    edad=fields.Char(string="Edad",compute="_get_edad",store=True)
    @api.depends("fecha_nac")
    def _get_edad(self):
        for a in self:
            if(a.fecha_nac):
                birthDate=a.fecha_nac
                today = date.today()
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                a.edad=str(age)+" Años"# Calcular edad
            else:
                a.edad ="0 Años"



class HrEmployeePersonDependen(models.Model):
    _name = 'hr.empl.person.depend'
    _description = 'HR Employee Personas con quien vive'
    _rac_name = "nombre_aplellido"
    payslip_run_id = fields.Many2one('hr.employee', string='empelado', readonly=True,
                                     copy=False,store=True )
    nombre_aplellido=fields.Char(string="Nombre y apellido",store=True)
    parentesco=fields.Char(string="Parentesco",store=True)
    cedula=fields.Char(string="cédula",store=True)
    fecha_nac=fields.Date(string="Fecha de Nacimiento",store=True)
    edad=fields.Char(string="Edad",compute="_get_edad",store=True)
    @api.depends("fecha_nac")
    def _get_edad(self):
        for a in self:
            if(a.fecha_nac):
                today = date.today()
                birthDate = a.fecha_nac
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                a.edad=str(age)+" Años"# Calcular edad
            else:
                a.edad ="0 Años"
