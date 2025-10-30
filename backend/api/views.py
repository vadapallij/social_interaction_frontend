from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProximityData, PedometerData, MotionData
from .serializers import ProximityDataSerializer, PedometerDataSerializer, MotionDataSerializer

@api_view(['GET'])
def proximity_list(request):
    items = ProximityData.objects.using('default').all()[:100]   # limit to 100 rows
    serializer = ProximityDataSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pedometer_list(request):
    items = PedometerData.objects.using('default').all()[:100]
    serializer = PedometerDataSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def motion_list(request):
    items = MotionData.objects.using('default').all()[:100]
    serializer = MotionDataSerializer(items, many=True)
    return Response(serializer.data)
