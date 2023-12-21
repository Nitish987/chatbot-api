from django.urls import path
from . import views

urlpatterns = [
    path('v1/bot/', views.Chatbot.as_view(), name='chatbot'),
]
