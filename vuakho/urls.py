from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Nối luồng URL từ app san_pham (Giả sử bạn đã có file urls.py trong app san_pham)
     path('', include('san_pham.urls')), 
]

# ĐOẠN CODE NÀY GIÚP MỞ KHÓA THƯ MỤC MEDIA ĐỂ HIỂN THỊ ẢNH
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)