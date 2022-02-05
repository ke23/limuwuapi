
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .api_v1 import api_v1


urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/", api_v1.urls),
    path('', include('clients.urls')),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



