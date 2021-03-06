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

    'name': 'Retentions SIFERE',

    'version': '1.0',

    'category': 'Accounting',

    'summary': 'Retenciones SIFERE',

    'author': 'OPENPYME S.R.L',

    'website': 'http://www.openpyme.com.ar',

    'depends': [
        'l10n_ar_retentions',
    ],

    'data': [
        'views/retention_sifere.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,

    'auto_install': False,

    'application': True,

    'description': 'Contempla retenciones',

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
