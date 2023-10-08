from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Parcel, ParcelLocker
from .serializers import ParcelSerializer, ParcelLockerSerializer


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'All Parcels': '/parcel/',
        'Add Parcel': '/parcel/create/',
        'Update Parcel': '/parcel/update/pk/',
        'Delete Parcel': '/parcel/delete/pk/',
        'All Parcel Lockers': '/parcel_locker/',
        'Add Parcel Locker': '/parcel_locker/create/',
        'Update Parcel Locker': '/parcel_locker/update/pk/',
        'Delete Parcel Locker': '/parcel_locker/delete/pk/',
        'Put Parcel To Locker': '/putparceltolocker/parcel/locker/',
        'Move Parcel Between Lockers': '/moveparcelbetweenlockers/parcel/locker_src/locker_dest/',
        'Take Parcel From Locker': '/takeparcelfromlocker/parcel/',
    }
    return Response(api_urls)


# CRUD for parcels
@api_view(['POST'])
def add_parcel(request):
    serializer = ParcelSerializer(data=request.data)
 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_parcels(request):
    snippets = Parcel.objects.all()
 
    if snippets:
        serializer = ParcelSerializer(snippets, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_parcel(request, pk):
    parcel = get_object_or_404(Parcel, pk=pk)
    serializer = ParcelSerializer(instance=parcel, data=request.data)
 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_parcel(request, pk):
    parcel = get_object_or_404(Parcel, pk=pk)
    parcel.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


#CRUD for parcel lockers
@api_view(['POST'])
def add_parcel_locker(request):
    serializer = ParcelLockerSerializer(data=request.data)
 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_parcel_lockers(request):
    snippets = ParcelLocker.objects.all()
 
    if snippets:
        serializer = ParcelLockerSerializer(snippets, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_parcel_locker(request, pk):
    parcel_locker =  get_object_or_404(ParcelLocker, pk=pk)
    serializer = ParcelLockerSerializer(instance=parcel_locker, data=request.data)
 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_parcel_locker(request, pk):
    parcel_locker = get_object_or_404(ParcelLocker, pk=pk)
    parcel_locker.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


# Endpoints for moving parcels between lockers
@api_view(['GET'])
def put_parcel_to_locker(request, parcel, locker):
    parcel_obj = get_object_or_404(Parcel, pk=parcel)
    locker_obj = get_object_or_404(ParcelLocker, pk=locker)
    
    # Check if pacel is not in some locker already
    if parcel_obj.locker_id:
        return Response({'Locker id': parcel_obj.locker_id.id}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if locker is free
    if locker_obj.status in ('BUSY', 'OOO',):
        return Response({'Locker status': locker_obj.status}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if parcel size fits locker size
    if not parcel_fits_locker_size(parcel_obj.parcel_size, locker_obj.locker_size):
        return Response({'Parcel size': parcel_obj.parcel_size, 'Locker size': locker_obj.locker_size},
                        status=status.HTTP_400_BAD_REQUEST
                        )
    
    # Add locker id to parcel record
    parcel_json = ParcelSerializer(parcel_obj).data
    parcel_json['locker_id'] = locker_obj.id
    parcel_serializer = ParcelSerializer(parcel_obj, data=parcel_json)
    
    # Set particular locker's status to "BUSY"
    locker_json = ParcelLockerSerializer(locker_obj).data
    locker_json['status'] = 'BUSY'
    locker_serializer = ParcelLockerSerializer(locker_obj, data=locker_json)
    
    if parcel_serializer.is_valid() and locker_serializer.is_valid():
        parcel_serializer.save()
        locker_serializer.save()
        return Response(parcel_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def move_parcel_between_lockers(request, parcel, locker_src, locker_dest):
    parcel_obj = get_object_or_404(Parcel, pk=parcel)
    locker_src_obj = get_object_or_404(ParcelLocker, pk=locker_src)
    locker_dest_obj = get_object_or_404(ParcelLocker, pk=locker_dest)
    
    # Check if destination locker is free
    if locker_dest_obj.status in ('BUSY', 'OOO',):
        return Response({'Destination locker status': locker_dest_obj.status}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if pacel is in some locker
    if not parcel_obj.locker_id:
        return Response({'Locker id': 'null'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if parcel size fits destination locker size
    if not parcel_fits_locker_size(parcel_obj.parcel_size, locker_dest_obj.locker_size):
        return Response({'Parcel size': parcel_obj.parcel_size, 'Destination locker size': locker_dest_obj.locker_size},
                        status=status.HTTP_400_BAD_REQUEST
                        )
    
    # Add locker id to parcel record
    parcel_json = ParcelSerializer(parcel_obj).data
    parcel_json['locker_id'] = locker_dest_obj.id
    parcel_serializer = ParcelSerializer(parcel_obj, data=parcel_json)
    
    # Set destination locker's status to "BUSY"
    locker_dest_json = ParcelLockerSerializer(locker_dest_obj).data
    locker_dest_json['status'] = 'BUSY'
    locker_dest_serializer = ParcelLockerSerializer(locker_dest_obj, data=locker_dest_json)
    
    # Set source locker's status to "FREE"
    locker_src_json = ParcelLockerSerializer(locker_src_obj).data
    locker_src_json['status'] = 'FREE'
    locker_src_serializer = ParcelLockerSerializer(locker_src_obj, data=locker_src_json)
    
    if parcel_serializer.is_valid() and locker_dest_serializer.is_valid() and locker_src_serializer.is_valid():
        parcel_serializer.save()
        locker_dest_serializer.save()
        locker_src_serializer.save()
        return Response(parcel_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def take_parcel_from_locker(request, parcel):
    parcel_obj = get_object_or_404(Parcel, pk=parcel)
    if not parcel_obj.locker_id:
        return Response({'Parcel locker id': parcel_obj.locker_id}, status=status.HTTP_400_BAD_REQUEST)
    locker_obj = get_object_or_404(ParcelLocker, pk=parcel_obj.locker_id.id)
    
    # Remove locker id from parcel record
    parcel_json = ParcelSerializer(parcel_obj).data
    parcel_json['locker_id'] = None
    parcel_serializer = ParcelSerializer(parcel_obj, data=parcel_json)
    
    # Set particular locker's status to "FREE"
    locker_json = ParcelLockerSerializer(locker_obj).data
    locker_json['status'] = 'FREE'
    locker_serializer = ParcelLockerSerializer(locker_obj, data=locker_json)
    
    if parcel_serializer.is_valid() and locker_serializer.is_valid():
        parcel_serializer.save()
        locker_serializer.save()
        return Response(parcel_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def parcel_fits_locker_size(parcel_size, locker_size):
    parcel_fits = True
    if parcel_size == 'XS':
        parcel_fits = True
    if parcel_size == 'S':
        if locker_size in ('XS',):
            parcel_fits = False
        else:
            parcel_fits = True
    if parcel_size == 'M':
        if locker_size in ('XS', 'S',):
            parcel_fits = False
        else:
            parcel_fits = True
    if parcel_size == 'L':
        if locker_size in ('XS', 'S', 'M',):
            parcel_fits = False
        else:
            parcel_fits = True
    if parcel_size == 'XL':
        if locker_size in ('XS', 'S', 'M', 'L',):
            parcel_fits = False
        else:
            parcel_fits = True
    return parcel_fits