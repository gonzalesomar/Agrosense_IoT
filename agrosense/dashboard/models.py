from django.db import models

# Create your models here.

# Services
class Feature(models.Model):
  name = models.CharField(max_length=100)
  details = models.CharField(max_length=500)

############################################################################################################################
# Resumen sensor 1
# Receives information about the humidity sensor at three differente positions
class SensorData_1(models.Model):
  battery_level = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_25 = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_50 = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_75 = models.DecimalField(max_digits=15, decimal_places=2)
  electrical_conductivity = models.DecimalField(max_digits=15, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-timestamp']
    
    def __str__(self):
      return (  f"Battery: {self.battery_level}%, "
                f"Humidity25: {self.humidity_25}%, "
                f"Humidity50: {self.humidity_50}%, "
                f"Humidity75: {self.humidity_75}%, "
                f"Conductivity: {self.electrical_conductivity} mS/cm "
                f"({self.timestamp:%B %d, %H:%M})")
      
############################################################################################################################      
# Resumen sensor 2
class SensorData_2(models.Model):
  battery_level = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_25 = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_50 = models.DecimalField(max_digits=15, decimal_places=2)
  humidity_75 = models.DecimalField(max_digits=15, decimal_places=2)
  electrical_conductivity = models.DecimalField(max_digits=15, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-timestamp']
    
    def __str__(self):
      return (  f"Battery: {self.battery_level}%, "
                f"Humidity25: {self.humidity_25}%, "
                f"Humidity50: {self.humidity_50}%, "
                f"Humidity75: {self.humidity_75}%, "
                f"Conductivity: {self.electrical_conductivity} mS/cm "
                f"({self.timestamp:%B %d, %H:%M})")
    
############################################################################################################################
class OnOff(models.Model):
    State = models.BooleanField(default=False)

    def str(self):
        return "On" if self.State else "Off"
    
