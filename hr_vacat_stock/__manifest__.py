# -*- coding: utf-8 -*-
{
    'name': "hr_vacat_stock",

    'summary': """
        Inventario de vacaciones""",

    'description': """
        Inventario de vacaciones
    """,

    'author': "Rimax Services, S. A.",
    'website': " ",


    'category': 'Human Resources/Employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_holidays','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_vacat_stock.xml',
        'views/hr_employee_views.xml',
        'views/hr_vacat_form.xml',
        'views/hr_leave_formulario.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
