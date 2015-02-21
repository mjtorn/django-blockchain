django-blockchain
=================

Wrap the Blockchain API in Django!

What's implemented
------------------

Accually is not much. The ``receive`` API.

Caveat
------

You must implement your own version of ``ReceiveNotification``! The reason is simply that you may have varying needs for how
to store things like the original JSON (See [django-psqljsonb](https://github.com/codento/django-psqljsonb)) or custom fields.

Creating the class is simple

    from django_blockchain.models import ReceiveNotificationBase

    class ReceiveNotification(ReceiveNotificationBase):
        """Fine with the defaults, thanks"""
        pass

Store the dotted path in settings

    BLOCKCHAIN_RECEIVE_NOTIFICATION_MODEL = 'yourapp.models.ReceiveNotification'

Installation
------------

    INSTALLED_APPS = (
        'django_blockchain',
    )

And something in your ``urls.py``

    urlpatterns = patterns('',
        url(r'^receive_notification$', 'django_blockchain.views.receive_notification', name='receive_notification'),
    )

Configuration
-------------

The following settings are optional

  * BLOCKCHAIN_API_KEY
  * BLOCKCHAIN_DESTINATION_ADDRESS

For receiving, you may want to configure these

  * BLOCKCHAIN_RECEIVE_API_ENDPOINT
  * BLOCKCHAIN_RECEIVE_NOTIFICATION_MODEL

This one is required if you use ``django_blockchain.views.receive_notification``

  * BLOCKCHAIN_RECEIVE_CONFIRMATION_LIMIT

Usage
-----

To create a new receiving address:

    res = models.ReceiveResponse.receive(YOUR_ADDRESS, YOUR_CALLBACK_URL)

or if you configured ``BLOCKCHAIN_DESTINATION_ADDRESS`` and ``BLOCKCHAIN_RECEIVE_API_ENDPOINT``:

    res = models.ReceiveResponse.receive()

For receiving notifications, make sure your ``urls.py`` has something like this:

    urlpatterns = urlpatterns('',
        url(r'^receive_notification', 'django_blockchain.views.receive_notification', name='receive_notification')
    )

