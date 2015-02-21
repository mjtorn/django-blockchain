from django.db import models

from blockchain import receive as bc_receive

from decimal import Decimal

from .settings import *  # NOQA

from . import utils


class ReceiveResponse(models.Model):
    """Store ReceiveResponse objects
    """

    fee_percent = models.IntegerField()
    destination_address = models.CharField(max_length=35)
    input_address = models.CharField(max_length=35)
    callback_url = models.URLField()

    def __unicode__(self):
        return u'{} -> {}'.format(self.input_address, self.destination_address)

    @staticmethod
    def receive(dest_addr=BLOCKCHAIN_DESTINATION_ADDRESS, cb_url=BLOCKCHAIN_RECEIVE_API_ENDPOINT, api_code=None):
        """Wrap the receive function here instead of the manager or wherever
        XXX: This method should be allowed to fail cleanly!
        """

        utils.check_addr(dest_addr)
        utils.check_cb_url(cb_url)

        res = bc_receive.receive(dest_addr, cb_url, api_code=api_code)

        new = ReceiveResponse()
        for field in ReceiveResponse._meta.get_all_field_names():
            if field == 'id':
                continue

            setattr(new, field, getattr(res, field))

        new.save()

        return new


class ReceiveNotificationBase(models.Model):
    """Once any BTC is received, store the notification
    """

    date_received = models.DateTimeField(auto_now_add=True)

    value = models.PositiveIntegerField(help_text='In satoshi')
    input_address = models.CharField(max_length=35)
    confirmations = models.PositiveIntegerField()
    transaction_hash = models.CharField(max_length=64)
    input_transaction_hash = models.CharField(max_length=64)
    destination_address = models.CharField(max_length=35)

    class Meta:
        """Make this abstract so you can handle custom parameters how you want
        Returns unsaved class; override this method to further deal with data
        """

        abstract = True

    @property
    def value_btc(self):
        """Satoshi -> BTC
        """

        if self.value is None:
            raise AttributeError('Need a value to divide')

        return Decimal(self.value) / 100000000

    @classmethod
    def parse_notification(cls, data):
        """Override this class to set data
        """

        fields = ReceiveNotificationBase._meta.get_all_field_names()

        new = cls()
        for field in fields:
            if field == 'date_received':
                continue

            setattr(new, field, data[field])

        return new

    def clean(self):
        """XXX: These should be fields' validators!
        """

        utils.check_tx_hash(self.transaction_hash)
        utils.check_tx_hash(self.input_transaction_hash)
        utils.check_addr(self.input_address)
        utils.check_addr(self.destination_address)

