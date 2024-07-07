from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's default authentication URLs
    path('accounts/', include('bank.urls')),  # Include your app's URLs
    path('', include('bank.urls')),  # Add your app’s URLs
]
