import hmac
import os
import subprocess
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Case, When, IntegerField
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import VideoProject, Article, DangKyTuVan

def _ordered_videos():
    # ÉP THỨ TỰ: NANO (1) -> M7.5 (2) -> JUMBO (3)
    return VideoProject.objects.annotate(
        custom_order=Case(
            When(phan_loai='NANO', then=1),
            When(phan_loai='M7.5', then=2),
            When(phan_loai='JUMBO', then=3),
            output_field=IntegerField(),
        )
    ).order_by('custom_order', '-ngay_tao')


def home_page(request):
    videos = _ordered_videos()
    context = {
        'videos': videos,
        'videos_youtube': videos.filter(nen_tang='YOUTUBE')[:4],
        'videos_tiktok': videos.filter(nen_tang='TIKTOK')[:4],
    }
    return render(request, 'home.html', context)

def blog_page(request):
    articles = Article.objects.filter(hien_thi=True)
    videos = _ordered_videos()
    context = {
        'articles': articles,
        'videos': videos,
        'videos_youtube': videos.filter(nen_tang='YOUTUBE')[:4],
        'videos_tiktok': videos.filter(nen_tang='TIKTOK')[:4],
    }
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
    return redirect('home_page')


@csrf_exempt
def deploy_webhook(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    token = request.META.get('HTTP_X_DEPLOY_TOKEN', '')
    expected = getattr(settings, 'DEPLOY_WEBHOOK_TOKEN', '')
    if not expected or not hmac.compare_digest(token, expected):
        return HttpResponse(status=403)

    repo = '/home/nhkeos0p/webvuakho'
    venv = '/home/nhkeos0p/virtualenv/webvuakho/3.12/bin'
    log = []
    try:
        for cmd in [
            ['git', 'fetch', 'origin', 'main'],
            ['git', 'reset', '--hard', 'origin/main'],
            [f'{venv}/pip', 'install', '-r', f'{repo}/requirements.txt', '-q'],
            [f'{venv}/python', 'manage.py', 'migrate', '--no-input'],
            [f'{venv}/python', 'manage.py', 'collectstatic', '--no-input'],
        ]:
            r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=120)
            log.append({'cmd': cmd[0], 'ok': r.returncode == 0, 'out': r.stdout[-500:], 'err': r.stderr[-500:]})
            if r.returncode != 0:
                return JsonResponse({'status': 'error', 'log': log}, status=500)

        with open(f'{repo}/tmp/restart.txt', 'w'):
            pass
        return JsonResponse({'status': 'ok', 'log': log})
    except Exception as e:
        return JsonResponse({'status': 'error', 'detail': str(e)}, status=500)