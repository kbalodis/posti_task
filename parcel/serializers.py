from rest_framework import serializers

from .models import Parcel, ParcelLocker


class ParcelLockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelLocker
        fields = ('id',
                  'locker_location_address',
                  'locker_size',
                  'status',
                  'created',
                  )


class ParcelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Parcel
        fields = ('id',
                  'sender', 
                  'sender_email', 
                  'sender_phone', 
                  'reciever', 
                  'reciever_email', 
                  'reciever_phone', 
                  'parcel_size',
                  'locker_id',
                  'created',
                  )
