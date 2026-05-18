from django.contrib import admin
from django.urls import path, include # Nhớ import thêm 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Nối tất cả các đường dẫn của app san_pham ra trang chủ
    path('', include('san_pham.urls')), 
]