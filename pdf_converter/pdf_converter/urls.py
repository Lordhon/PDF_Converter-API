
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from converter.views import TxtToPdfConverter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('converter',TxtToPdfConverter.as_view() , name='converter')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

