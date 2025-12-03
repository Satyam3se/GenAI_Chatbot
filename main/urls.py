from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
