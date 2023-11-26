from django.urls import path
from . import views


urlpatterns = [
    path('v1/auth/', views.CustomerAuth.as_view(), name='customer-auth'),
]