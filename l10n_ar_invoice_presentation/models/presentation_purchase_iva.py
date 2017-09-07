# - coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp import models
import l10n_ar_api.presentations.presentation as presentation_builder
from presentation_tools import PresentationTools
from presentation_purchase import PurchaseInvoicePresentation


class PurchaseIvaPresentation:
    def __init__(self, proxy=None, date_from=None, date_to=None, with_prorate=False):
        self.invoice_proxy = proxy
        self.date_from = date_from
        self.date_to = date_to
        self.with_prorate = with_prorate
        self.get_general_data()

    # Datos del sistema
    def get_general_data(self):
        "Obtiene valores predeterminados de la localizacion"
        self.type_b = self.invoice_proxy.env.ref('l10n_ar_afip_tables.account_denomination_b')
        self.type_c = self.invoice_proxy.env.ref('l10n_ar_afip_tables.account_denomination_c')
        self.type_d = self.invoice_proxy.env.ref('l10n_ar_afip_tables.account_denomination_d')
        self.type_i = self.invoice_proxy.env.ref('l10n_ar_afip_tables.account_denomination_i')
        self.tax_group_vat = self.invoice_proxy.env.ref('l10n_ar.tax_group_vat')

    def get_invoices(self):
        """
        Trae las facturas para generar la presentacion de compras.
        :return: recordset, Las facturas de compras.
        """
        invoices = self.invoice_proxy.search([
            ('type', 'in', ('in_invoice', 'in_refund')),
            ('state', 'not in', ('cancel', 'draft')),
            ('date_invoice', '>=', self.date_from),
            ('date_invoice', '<=', self.date_to),
            ('denomination_id', 'not in', [
                self.type_b.id,
                self.type_c.id,
                self.type_d.id,
                self.type_i.id,
            ])
        ])
        return invoices

    def create_line(self, builder, invoice, helper):
        """
        Crea x lineas por cada factura, segun la cantidad de alicuotas usando el builder y el helper
        para todas las facturas que no son de importacion.
        :param builder: objeto de la api para construir las lineas de la presentacion
        :param invoice: record, factura
        :param helper: objeto con metodos auxiliares
        """
        if PurchaseInvoicePresentation.get_purchase_cantidadAlicIva(invoice,self.type_b,self.type_c,self.tax_group_vat) > 0:
            for tax in invoice.tax_line_ids:
                if (
                    tax.tax_id.tax_group_id == self.tax_group_vat
                    or PurchaseInvoicePresentation.get_purchase_codigoOperacion(invoice, self.type_d) == 'N'
                ):
                    line = builder.create_line()
                    rate = helper.get_currency_rate_from_move(invoice)
                    line.tipoComprobante = PurchaseInvoicePresentation.get_purchase_tipo(invoice, helper)
                    line.puntoDeVenta = PurchaseInvoicePresentation.get_purchase_puntoDeVenta(invoice,self.type_d)
                    line.numeroComprobante = PurchaseInvoicePresentation.get_purchase_numeroComprobante(invoice,self.type_d)
                    line.codigoDocVend = PurchaseInvoicePresentation.get_purchase_codigoDocumento(invoice)
                    line.numeroIdVend = PurchaseInvoicePresentation.get_purchase_numeroVendedor(invoice)
                    line.importeNetoGravado = self.get_purchase_vat_importeNetoGravado(tax, rate, helper)
                    line.alicuotaIva = self.get_purchase_vat_alicuotaIva(tax, PurchaseInvoicePresentation.get_purchase_codigoOperacion(invoice, self.type_d))
                    line.impuestoLiquidado = helper.format_amount(rate * tax.amount)

    # ----------------CAMPOS ALICUOTAS----------------
    # Campo 6
    @staticmethod
    def get_purchase_vat_importeNetoGravado(tax, rate, helper):
        return helper.format_amount(tax.base * rate)

    # Campo 7
    @staticmethod
    def get_purchase_vat_alicuotaIva(tax, operation_code):
        """
        Si la operacion es exenta o no gravada se devuelve 3. Sino se devuelve el codigo de impuesto
        :param tax: objeto impuesto
        :param operation_code: char codigo de operacion
        """
        if operation_code in ['E', 'N']:
            return '3'

        codes_model_proxy = tax.env['codes.models.relation']

        tax_code = codes_model_proxy.get_code(
            'account.tax',
            tax.tax_id.id
        )

        return tax_code


class AccountInvoicePresentation(models.Model):

    _inherit = 'account.invoice.presentation'

    def generate_purchase_vat_file(self):
        """
        Se genera el archivo de alicuotas de compras. Utiliza la API de presentaciones y tools para poder crear los archivos
        y formatear los datos.
        :return: objeto de la api (generator), con las lineas de la presentacion creadas.
        """
        # Instanciamos API, tools y datos generales
        builder = presentation_builder.Presentation('ventasCompras', 'comprasAlicuotas')
        helper = PresentationTools()
        presentation = PurchaseIvaPresentation(
            proxy=self.env["account.invoice"],
            date_from=self.date_from,
            date_to=self.date_to,
            with_prorate=self.with_prorate
        )

        # Se traen todas las facturas de compra del periodo indicado
        invoices = presentation.get_invoices()
        # Validamos que se tengan los datos necesarios de los partners.
        self.validate_invoices(invoices)

        # Se crea la linea de la presentacion para cada factura.
        map(
            lambda invoice: presentation.create_line(
                builder, invoice, helper
            ), invoices
        )
        return builder

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
