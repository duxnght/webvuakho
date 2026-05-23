from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, IntegerField
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import VideoProject, Article, DangKyTuVan

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

@require_POST
def dang_ky_tu_van(request):
    phone = request.POST.get('phone', '').strip()
    tinh_thanh = request.POST.get('address', '').strip()

    if not phone or not tinh_thanh:
        return JsonResponse({'status': 'error', 'message': 'Vui lòng điền đầy đủ thông tin.'})

    digits = phone.replace('+', '').replace(' ', '').replace('-', '')
    if not digits.isdigit() or not (9 <= len(digits) <= 15):
        return JsonResponse({'status': 'error', 'message': 'Số điện thoại không hợp lệ.'})

    DangKyTuVan.objects.create(so_dien_thoai=phone, tinh_thanh=tinh_thanh)
    return JsonResponse({'status': 'success'})

def danh_muc_du_an(request):
    pass