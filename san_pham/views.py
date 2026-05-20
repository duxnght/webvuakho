from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, IntegerField
from .models import VideoProject, Article

def home_page(request):
    # Lấy danh sách video và ÉP THỨ TỰ: NANO (1) -> M7.5 (2) -> JUMBO (3)
    videos = VideoProject.objects.annotate(
        custom_order=Case(
            When(phan_loai='NANO', then=1),
            When(phan_loai='M7.5', then=2),
            When(phan_loai='JUMBO', then=3),
            output_field=IntegerField(),
        )
    ).order_by('custom_order', '-ngay_tao')
    
    context = {'videos': videos}
    return render(request, 'home.html', context)

def blog_page(request):
    articles = Article.objects.filter(hien_thi=True)
    context = {'articles': articles}
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    article = get_object_or_404(Article, duong_dan_alias=slug, hien_thi=True)
    context = {'article': article}
    return render(request, 'blog_detail.html', context)

def tai_lieu_page(request):
    return render(request, 'tailieu.html')

def dang_ky_tu_van(request):
    pass

def danh_muc_du_an(request):
    pass