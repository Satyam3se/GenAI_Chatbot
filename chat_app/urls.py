from django.urls import path
from . import views

app_name = 'chat_app'
urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('send_message/', views.send_message, name='send_message'),
    path('history/', views.get_chat_history, name='get_chat_history'),
]
