from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature
from .models import SensorData_1, SensorData_2, OnOff
from django.utils import timezone
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import SensorData1_serializer1, SensorData1_serializer2, SensorData2_serializer1, SensorData2_serializer2
from .forms import OnOff_Form

# Create your views here.

def index(request):
  
  feature1 = Feature()
  feature1.id = 0
  feature1.name = 'Monitoreo y Control Remoto en Tiempo Real'
  feature1.details= 'Proporcionamos un sistema integral que permite a los usuarios monitorear y controlar sus sistemas de riego en tiempo real desde cualquier dispositivo con acceso a internet. '
  
  
  feature2 = Feature()
  feature2.id = 1
  feature2.name = 'Datos y Gráficos Informativos'
  feature2.details= 'Ofrecemos herramientas avanzadas de análisis de datos y gráficos informativos que ayudan a los usuarios a entender mejor el rendimiento de su sistema de riego y la salud de sus cultivos.'
  
    
  feature3 = Feature()
  feature3.id = 2
  feature3.name = 'Seguridad y Protección de Datos'
  feature3.details= 'Garantizamos la seguridad y privacidad de los datos recopilados por nuestro sistema de monitoreo de riego IoT. Implementamos protocolos avanzados de encriptación y autenticación para proteger la información de nuestros usuarios contra accesos no autorizados y ciberamenazas.'
  
  
  features = [feature1, feature2, feature3]
  
  return render(request, 'index.html', {'features': features})  
  
  """
  features = Feature.objects.all()
  return render(request, 'index.html', {'features': features})  
  """

def register(request):
  
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username already used')
        return redirect('register')
      elif User.objects.filter(email=email).exists():
        messages.info(request, 'Email already used')
        return redirect('register')
      else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save();
        return redirect('login')
    else:
      messages.info(request, 'Password not the same')
      return redirect('register')
    
  else: 
    return render(request, 'register.html')
   
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
      auth.login(request, user)
      return redirect('/')
    else:
      messages.info(request, 'Credentials invalid')
      return redirect('login')
  else:
    return render(request, 'login.html')  
  
def logout(request):
  auth.logout(request)  
  return redirect('/')

def counter(request):
  posts = [1, 2, 3, 4, 5, 'david', 'miranda', 'zarate']
  return render(request, 'counter.html', {'posts':posts}) 

def post(request, pk):
  return render(request, 'post.html', {'pk':pk})

def index_dashboard(request):
    onoff_instance = OnOff.objects.first()  # Assuming there's only one OnOff instance

    if request.method == 'POST':
        form = OnOff_Form(request.POST, instance=onoff_instance)
        if form.is_valid():
            form.save()
            return redirect('index_dashboard')  # Adjust redirect as needed
    else:
        form = OnOff_Form(instance=onoff_instance)

    return render(request, 'index_dashboard.html', {
        'form': form,
        'onoff_state': onoff_instance.State if onoff_instance else None
    })

def stats(request):
  return render(request, 'stats.html')

def help(request):
  return render(request, 'help.html')
    
def command_serializer(request):
    if request.method == 'GET':
        data = {}
        # Attempt to fetch the latest entry for each sensor data
        for sensor_model, sensor_prefix in [(SensorData_1, '1'), (SensorData_2, '2')]:
            try:
                latest_entry = sensor_model.objects.latest('timestamp')
                data.update({
                    f'battery_level_{sensor_prefix}': latest_entry.battery_level,
                    f'humidity_25_{sensor_prefix}': latest_entry.humidity_25,
                    f'humidity_50_{sensor_prefix}': latest_entry.humidity_50,
                    f'humidity_75_{sensor_prefix}': latest_entry.humidity_75,
                    f'electrical_conductivity_{sensor_prefix}': latest_entry.electrical_conductivity,
                })
            except ObjectDoesNotExist:
                data[f'error_{sensor_prefix}'] = f'No sensor data available in sensor {sensor_prefix}'

        if not data:
            # If no data was added, return an error
            return JsonResponse({'error': 'No sensor data available'}, status=404)

        # Return the data as JSON
        return JsonResponse(data)
    
def get_last_entries(request):
    if request.method == 'GET':
        data = {}
        for sensor_model, sensor_prefix in [(SensorData_1, '1'), (SensorData_2, '2')]:
            entries = sensor_model.objects.order_by('-timestamp')[:24]
            entries_data = []
            for entry in entries:
                entries_data.append({
                    'timestamp': entry.timestamp.strftime('%m-%d %H:%M'),
                    'battery_level': entry.battery_level,
                    'humidity_25': entry.humidity_25,
                    'humidity_50': entry.humidity_50,
                    'humidity_75': entry.humidity_75,
                    'electrical_conductivity': entry.electrical_conductivity,
                })
            data[f'sensor_{sensor_prefix}_last_10_entries'] = entries_data

        if not data:
            return JsonResponse({'error': 'No sensor data available'}, status=404)

        return JsonResponse(data)


@csrf_exempt
def Agrosense_serializer_add_data_sensor1(request):
    if request.method == 'POST':  # Comunicación con ESP32
        data = JSONParser().parse(request)
        serializer = SensorData1_serializer1(data=data)
        if serializer.is_valid():
            sensor_data_instance = serializer.save()
            sensor_data_instance.battery_level = data['battery_level']*10
            sensor_data_instance.humidity_25 = data['humidity_25']
            sensor_data_instance.humidity_50 = data['humidity_50']
            sensor_data_instance.humidity_75 = data['humidity_75']
            sensor_data_instance.electrical_conductivity = data['electrical_conductivity']
            sensor_data_instance.save(update_fields=["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity"])
            return HttpResponse(serializer.data, status=201)

     
@csrf_exempt 
def Agrosense_serializer_add_data_sensor2(request):
    if request.method == 'POST':  # Comunicación con ESP32
        data = JSONParser().parse(request)
        serializer = SensorData2_serializer1(data=data)
        if serializer.is_valid():
            sensor_data_instance = serializer.save()
            sensor_data_instance.battery_level = data['battery_level']
            sensor_data_instance.humidity_25 = data['humidity_25']
            sensor_data_instance.humidity_50 = data['humidity_50']
            sensor_data_instance.humidity_75 = data['humidity_75']
            sensor_data_instance.electrical_conductivity = data['electrical_conductivity']
            sensor_data_instance.save(update_fields=["battery_level", "humidity_25", "humidity_50", "humidity_75", "electrical_conductivity"])
            return HttpResponse(serializer.data, status=201)


@csrf_exempt
def Send_State(request):
    # Get the first instance
    last_state = OnOff.objects.all().first()
    
    # Prepare the response data
    response_data = {
        'state': bool(last_state.State) if last_state else None,
    }
    
    # Get all instances
    all_states = OnOff.objects.all()
    
    # Check if there are more than one instance
    if all_states.count() > 1:
        # Delete all objects except the first one
        OnOff.objects.exclude(pk=last_state.pk).delete()
    
    return JsonResponse(data=response_data)