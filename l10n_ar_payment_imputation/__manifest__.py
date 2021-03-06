# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{

    'name': 'l10n_ar_payment_imputation',

    'version': '1.0',

    'category': 'Accounting',

    'summary': 'Imputaciones de pagos',

    'author': 'OPENPYME S.R.L',

    'website': 'http://www.openpyme.com.ar',

    'depends': [
        'l10n_ar_account_payment',
    ],

    'data': [
        'views/account_payment_view.xml',
        'wizard/register_payment_view.xml',
        'wizard/account_payment_imputation_view.xml',
        'static/xml/create_payment_asset.xml',
        'security/ir.model.access.csv'
    ],

    'qweb': [
        'static/xml/create_payment.xml'
    ],

    'installable': True,

    'auto_install': False,

    'application': True,

    'description': """
Imputaciones de pagos
========================================
    Pagos de multiples facturas total y parcialmente
    """,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
