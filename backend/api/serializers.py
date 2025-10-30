from rest_framework import serializers
from .models import ProximityData, PedometerData, MotionData  # adjust names

class ProximityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProximityData
        fields = '__all__'

class PedometerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedometerData
        fields = '__all__'

class MotionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionData
        fields = '__all__'
