from django.urls import path
from . import views

urlpatterns = [
    path('v1/bot/', views.Chatbot.as_view(), name='chatbot'),
    path('v1/bot-greetings/', views.ChatbotGreetings.as_view(), name='chatbot-greetings'),
    path('v1/bot-emform/', views.ChatbotEmformSubmit.as_view(), name='chatbot-emform'),
]
