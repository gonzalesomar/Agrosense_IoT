from rest_framework import serializers
from .models import SensorData_1, SensorData_2, OnOff
""""""
class SensorData1_serializer1(serializers.ModelSerializer): # Post (ESP32)
  class Meta:
    model = SensorData_1
    fields = ["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity"]
  
  
class SensorData2_serializer1(serializers.ModelSerializer): # Post (ESP32)
  class Meta:
    model = SensorData_2
    fields = ["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity"]
    
    
class SensorData1_serializer2(serializers.ModelSerializer): # Visualizar en HTTP
  class Meta:
    model = SensorData_1
    fields = ["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity", "timestamp"]
  
  
class SensorData2_serializer2(serializers.ModelSerializer): # Visualizar en HTTP
  class Meta:
    model = SensorData_2
    fields = ["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity", "timestamp"]


class OnOff_serializer(serializers.ModelSerializer): #POST (ESP32)
    class Meta:
        model = OnOff
        fields=["State"]