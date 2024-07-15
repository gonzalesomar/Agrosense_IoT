from django.urls import path
from . import views
from .views import command_serializer, get_last_entries, Send_State

urlpatterns = [
  path('', views.index, name='index'),
  path('counter',views.counter, name='counter'),
  path('register',views.register, name='register'),
  path('login',views.login, name='login'),
  path('logout',views.logout, name='logout'),
  path('post/<str:pk>', views.post, name='post'),
  path('index_dashboard',views.index_dashboard, name='index_dashboard'),
  path('stats',views.stats, name='stats'),
  path('help',views.help, name='help'),
  path('get-sensor-data/', command_serializer, name='get_sensor_data'),
  path('get-sensor-chart/', get_last_entries, name='get-sensor-chart'),
  path('Sensor1/', views.Agrosense_serializer_add_data_sensor1, name='Listado_sensor1'),
  path('Sensor2/', views.Agrosense_serializer_add_data_sensor2, name='Listado_sensor2'),
  path('send-state/', Send_State, name='Send_State'),
]