# -*- coding: utf-8 -*-
{
    'name': 'UAE Payroll',
    'version': '1.0',
    'category': 'HR',
    'author':'Senthilnathan G,MaxVueTech',
    'website':'http://maxvuetech.com',
    'summary': 'UAE Payroll',
    'description': """
        Employee Master
        Accounting Conifguration to post entries
        Payslip Payment (Batchwise)
        SIF File Generation Batchwise
        Gratuity Calculation
        Expense Payment via Payslip
        """,
    'depends': [
                'hr',
                'hr_payroll_account',
                'hr_payroll',
                'account',
                'web_highcharts',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_payroll_data.xml',
        'wizard/hr_payslip_sif_generation_view.xml',
        'wizard/hr_payslip_batchwise_sif_generation_view.xml',
        'wizard/hr_payroll_register_payment.xml',
        'wizard/hr_payroll_batchwise_register_payment.xml',
        'wizard/hr_employee_gratuity_view.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payroll_dashboard.xml',
        'views/report_payslip_templates.xml',
        'views/report_payslipdetails_templates.xml',
        'wizard/payslip_confirm_state_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
