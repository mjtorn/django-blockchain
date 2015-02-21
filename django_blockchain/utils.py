from django.core import validators

HASH_LEN = 64
MIN_ADDR_LEN = 26
MAX_ADDR_LEN = 36


def check_tx_hash(tx_hash):
    """Does the input look like a hash?
    """

    if not tx_hash.isalnum():
        raise validators.ValidationError('tx_hash must be alphanumeric')

    if len(tx_hash) != HASH_LEN:
        raise validators.ValidationError('tx_hash length not {}'.format(HASH_LEN))


def check_addr(dest_addr):
    """Does the input look like a bitcoin address?
    """

    if not dest_addr.isalnum():
        raise validators.ValidationError('dest_addr must be alphanumeric')

    if not MIN_ADDR_LEN <= len(dest_addr) <= MAX_ADDR_LEN:
        raise validators.ValidationError('dest_addr length between {} and {}'.format(MIN_ADDR_LEN, MAX_ADDR_LEN))


def check_cb_url(cb_url):
    """Is our callback url a url?
    """

    validator = validators.URLValidator()

    validator(cb_url)

