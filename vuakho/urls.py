from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from san_pham.ckeditor_views import upload as ckeditor_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/upload/', ckeditor_upload, name='ckeditor_upload'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain; charset=utf-8')),
    path('llms.txt',   TemplateView.as_view(template_name='llms.txt',   content_type='text/plain; charset=utf-8')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml; charset=utf-8')),
    path('', include('san_pham.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
