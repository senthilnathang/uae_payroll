# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import os.path
import base64
import time

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from werkzeug import url_encode
from datetime import date, datetime
from time import gmtime, strftime

_logger = logging.getLogger(__name__)


class HrPayslipBatchwiseSifGeneration(models.TransientModel):

    _name = "hr.payslip.batchwise.sif.generation.wizard"
    _description = "Expense Payslip Sif Generation"

    batch_id = fields.Many2one('hr.payslip.run','Batch Name')
    company_bank_account_id = fields.Many2one('hr.company.bank.accounts', string="Company Bank Account Number")
    summary = fields.Binary('Employee Payslip Report', attachment=True,  readonly=True)
    company_id = fields.Many2one('res.company', string='Company')
    file_name = fields.Char('file name')

    @api.multi
    def expense_post_payment(self):
        self.ensure_one()
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        payslips = self.env['hr.payslip'].browse(active_ids)
        cwd = os.path.abspath(__file__)
        path = cwd.rsplit('/', 2)
        n_edr = 0
        tot_sal = 0
        png_file = open('salary.sif', "w")
        data11 = ''
        company_mol_id = self.company_bank_account_id.company_id.mol_id
        company_routing_code = self.company_bank_account_id.routing_code
        iban = self.company_bank_account_id.iban
        creation_date=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        creation_time=time.strftime("%H%M",time.gmtime(time.time()+14400))
        salary_month=time.strftime("%m%Y",time.localtime(time.time()))
        total_salary = 0.0
        for payslip in self.batch_id.slip_ids:
            mol_id = payslip.employee_id.mol_id
            start_date = payslip.date_from
            end_date=payslip.date_to
            d1 = datetime.strptime(start_date, "%Y-%m-%d")
            d2 = datetime.strptime(end_date, "%Y-%m-%d")
            daysDiff = abs((d2 - d1).days + 1)
            employee_iban = ''
            for line in payslip.employee_id.employee_bank_account_id:
                if line.default_bank_account == True:
                    employee_iban = line.iban
                    routing_code = line.routing_code

            png_file.write('EDR,')
            png_file.write(str(mol_id)+',')
            png_file.write(str(routing_code)+',')
            png_file.write(str(employee_iban)+',')
            png_file.write(str(start_date)+',')
            png_file.write(str(end_date)+',')
            png_file.write(str(daysDiff)+',')
            png_file.write(str(payslip.total_amount)+',')
            png_file.write('0,')
            png_file.write('0'+"\r\n")
            n_edr += 1
            total_salary += payslip.total_amount

        png_file.write('SCR,')
        png_file.write(str(company_mol_id) + ',')
        png_file.write(str(company_routing_code) + ',')
        png_file.write(str(creation_date) + ',')
        png_file.write(str(creation_time) + ',')
        png_file.write(str(salary_month) + ',')
        png_file.write(str(n_edr) + ',')
        png_file.write(str(total_salary) + ',')
        png_file.write('AED,')
        png_file.write('Inteslar Salary Process')

        zeros = ''
        if len(company_mol_id) != 12:
            value = 12 - len(company_mol_id)
            zeros = '0'
            for line in range(value):
                zeros = zeros + '0'
            total_value = zeros+company_mol_id
        else:
            total_value = company_mol_id

        file_cr_date = time.strftime("%y%m%d", time.localtime(time.time()))
        f_name = str(total_value) +str(file_cr_date)+str(creation_time)

        png_file.close()
        png_file = open('salary.sif', 'rb')
        data = png_file.read()
        # Pass your text file data using encoding.
        values = {
            'name': "Name of text file.txt",
            'datas_fname': str(f_name)+'00.sif',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(data),
        }
        png_file.close()

        attachment_id = self.env['ir.attachment'].sudo().create(values)
        # Prepare your download URL
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

       
