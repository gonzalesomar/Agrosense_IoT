from django import forms
from.models import SensorData_1, SensorData_2, OnOff

class CommandForm_1(forms.ModelForm):
  class Meta:
    model = SensorData_1
    fields = ['battery_level', 'humidity_25', 'humidity_50', 'humidity_75', 'electrical_conductivity']  # Using a list
    widgets = {
        'battery_level': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_25': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_50': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_75': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'electrical_conductivity': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          })
    }
    
class CommandForm_2(forms.ModelForm):
  class Meta:
    model = SensorData_2
    fields = ['battery_level', 'humidity_25', 'humidity_50', 'humidity_75', 'electrical_conductivity']  # Using a list
    widgets = {
        'battery_level': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_25': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_50': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'humidity_75': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          }),
        'electrical_conductivity': forms.NumberInput(attrs={
          'class': 'py-2 px-2 rounded-xl border'
          })
    }
    
class OnOff_Form(forms.ModelForm):
    class Meta:
        model = OnOff
        fields = ['State']
        widgets = {
            'State': forms.CheckboxInput(attrs={
                'class': 'py-2 px-2 rounded-xl border'
            })
        }