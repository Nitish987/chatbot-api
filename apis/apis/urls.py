from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    
    # API
    path('customer/', include('app.customer.urls')),
    path('chatbot/', include('app.chatbot.urls')),
]
