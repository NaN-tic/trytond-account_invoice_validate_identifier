# This file is part account_invoice_validate_identifier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import PoolMeta, Pool
from trytond.i18n import gettext
from trytond.exceptions import UserWarning


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    @ModelView.button
    @Workflow.transition('posted')
    def post(cls, invoices):
        super(Invoice, cls).post(invoices)
        for invoice in invoices:
            if invoice.state in ['draft', 'cancelled']:
                continue
            invoice.check_party_identifier()

    def check_party_identifier(self):
        Warning = Pool().get('res.user.warning')
        if not self.party.tax_identifier:
            key = 'invoice.party.identifier%s_%s' % (
                self.id, self.party.id)

            if Warning.check(key):
                raise UserWarning(key, gettext(
                    'account_invoice_validate_identifier.missing_party_identifier',
                    party=self.party.rec_name,
                    invoice=self.rec_name))
