# -*- coding: utf-8 -*-
# from odoo import http


# class HrVacatStock(http.Controller):
#     @http.route('/hr_vacat_stock/hr_vacat_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_vacat_stock/hr_vacat_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_vacat_stock.listing', {
#             'root': '/hr_vacat_stock/hr_vacat_stock',
#             'objects': http.request.env['hr_vacat_stock.hr_vacat_stock'].search([]),
#         })

#     @http.route('/hr_vacat_stock/hr_vacat_stock/objects/<model("hr_vacat_stock.hr_vacat_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_vacat_stock.object', {
#             'object': obj
#         })
