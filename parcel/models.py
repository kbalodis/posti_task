from django.db import models
from django.utils.translation import gettext_lazy as _

    
class ParcelLocker(models.Model):
    class LockerSize(models.TextChoices):
        EXTRA_SMALL = 'XS', _('Extra small')
        SMALL = 'S', _('Small')
        MEDIUM = 'M', _('Medium')
        LARGE = 'L', _('Large')
        EXTRA_LARGE = 'XL', _('Extra large')
        
    class LockerStatus(models.TextChoices):
        FREE = 'FREE', _('Free')
        BUSY = 'BUSY', _('Busy')
        OUT_OF_ORDER = 'OOO', _('Out of order')

    locker_location_address = models.CharField(max_length=255)
    locker_size = models.CharField(
        max_length=2,
        choices=LockerSize.choices,
        default=LockerSize.SMALL,
    )
    status = models.CharField(
        max_length=4,
        choices=LockerStatus.choices,
        default=LockerStatus.FREE,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return self.locker_location_address


class Parcel(models.Model):
    class ParcelSize(models.TextChoices):
        EXTRA_SMALL = 'XS', _('Extra small')
        SMALL = 'S', _('Small')
        MEDIUM = 'M', _('Medium')
        LARGE = 'L', _('Large')
        EXTRA_LARGE = 'XL', _('Extra large')

    sender = models.CharField(max_length=255)
    sender_email = models.CharField(max_length=255)
    sender_phone = models.CharField(max_length=255)  
    reciever = models.CharField(max_length=255)
    reciever_email = models.CharField(max_length=255)
    reciever_phone = models.CharField(max_length=255)
    parcel_size = models.CharField(
        max_length=2,
        choices=ParcelSize.choices,
        default=ParcelSize.SMALL,
    )
    locker_id = models.ForeignKey(ParcelLocker, related_name='parcels', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return self.sender