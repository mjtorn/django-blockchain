from django.utils.module_loading import import_string
from django.http import HttpResponse
from django.conf import settings

from . import models


def receive_notification(request):
    """Imports your ReceiveNotification class and uses it
    """

    if settings.BLOCKCHAIN_RECEIVE_CONFIRMATION_LIMIT is None:
        raise ValueError('Need settings.BLOCKCHAIN_RECEIVE_CONFIRMATION_LIMIT')

    cls = import_string(settings.BLOCKCHAIN_RECEIVE_NOTIFICATION_MODEL)

    notification = cls.parse_notification(request.GET.copy())

    # Unhandled exceptions should be mailed to admins
    notification.full_clean()

    # One last thing, check this is not spam!
    rec_exists = models.ReceiveResponse.objects.filter(
        destination_address=notification.destination_address,
        input_address=notification.input_address,
    ).exists()

    if rec_exists:
        notification.save()
    else:
        return HttpResponse('Spam ignored', content_type='text/plain')

    if notification.confirmations >= settings.BLOCKCHAIN_RECEIVE_CONFIRMATION_LIMIT:
        return HttpResponse('*ok*', content_type='text/plain')

    return HttpResponse('More confirmations required', content_type='text/plain')

