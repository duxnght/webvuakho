from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('tai-lieu/', views.tai_lieu_page, name='tai_lieu_page'),
    path('dang-ky/', views.dang_ky_tu_van, name='dang_ky_tu_van'),
    path('du-an/', views.danh_muc_du_an, name='danh_muc_du_an'),
    path('blog/', views.blog_page, name='blog_page'),
    # Thêm đường dẫn cho trang đọc chi tiết bài viết
    path('blog/chi-tiet/', views.blog_detail, name='blog_detail'),
]