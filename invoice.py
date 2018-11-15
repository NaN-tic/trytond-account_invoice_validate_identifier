# This file is part account_invoice_validate_identifier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Invoice']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls._error_messages.update({
                'missing_party_identifier': ('There is no identifer on party '
                    '"%(party)s" and invoice "%(invoice)s".'),
                })

    @classmethod
    def validate(cls, invoices):
        super(Invoice, cls).validate(invoices)
        for invoice in invoices:
            if invoice.state in ['draft', 'cancel']:
                continue
            invoice.check_party_identifier()

    def check_party_identifier(self):
        if not self.party.identifiers:
            key = 'invoice.party.identifier%s_%s' % (
                self.id, self.party.id)
            self.raise_user_warning(key, 'missing_party_identifier', {
                    'party': self.party.rec_name,
                    'invoice': self.rec_name,
                    })
