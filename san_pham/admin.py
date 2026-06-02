import csv
import json
import os
import urllib.parse
import urllib.request
from io import BytesIO
from django.contrib import admin
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.utils import timezone
from PIL import Image as PilImage
from .models import VideoProject, Article, DangKyTuVan

admin.site.site_header = "Hệ thống Quản trị Vữa Khô Sông Hồng"
admin.site.site_title = "Admin Sông Hồng"
admin.site.index_title = "Bảng điều khiển"


def _to_webp(uploaded_file, quality=85):
    """Convert any uploaded image to WebP. Returns ContentFile or None on failure."""
    try:
        uploaded_file.seek(0)
        img = PilImage.open(uploaded_file)
        img.load()
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            bg = PilImage.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        buf = BytesIO()
        img.save(buf, format='WebP', quality=quality, method=4)
        buf.seek(0)
        base = os.path.splitext(os.path.basename(uploaded_file.name))[0]
        return ContentFile(buf.read(), name=f'{base}.webp')
    except Exception:
        return None


def _fetch_tiktok_thumbnail(url):
    """Lấy thumbnail TikTok qua oEmbed (best-effort, có thể thất bại)."""
    try:
        api = 'https://www.tiktok.com/oembed?url=' + urllib.parse.quote(url, safe='')
        req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('thumbnail_url') or ''
    except Exception:
        return ''


@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'nen_tang', 'phan_loai', 'sap_ra_mat', 'ngay_tao')
    list_filter = ('nen_tang', 'phan_loai', 'sap_ra_mat')
    search_fields = ('tieu_de',)

    fieldsets = (
        ('Thông tin video', {
            'fields': ('tieu_de', 'phan_loai', 'nen_tang', 'sap_ra_mat')
        }),
        ('Nguồn video', {
            'fields': ('link_youtube', 'link_tiktok', 'anh_thumbnail'),
            'description': 'Chọn nền tảng ở trên, rồi dán link tương ứng. TikTok nên tải kèm ảnh thumbnail (nếu để trống hệ thống sẽ thử tự lấy).'
        }),
    )

    def save_model(self, request, obj, form, change):
        # Chuyển thumbnail tải lên sang WebP
        if 'anh_thumbnail' in form.changed_data and form.cleaned_data.get('anh_thumbnail'):
            webp = _to_webp(form.cleaned_data['anh_thumbnail'])
            if webp:
                obj.anh_thumbnail.save(webp.name, webp, save=False)
        # TikTok không có thumbnail tải lên → thử lấy tự động qua oEmbed
        if obj.nen_tang == 'TIKTOK' and not obj.anh_thumbnail and obj.link_tiktok:
            obj.thumbnail_url = _fetch_tiktok_thumbnail(obj.link_tiktok)
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'tac_gia', 'hien_thi', 'ngay_dang')
    list_filter = ('hien_thi', 'ngay_dang', 'tac_gia')
    search_fields = ('tieu_de', 'tac_gia')
    prepopulated_fields = {'duong_dan_alias': ('tieu_de',)}

    fieldsets = (
        ('Thông tin bài viết', {
            'fields': ('tieu_de', 'tac_gia', 'anh_dai_dien', 'mo_ta_ngan', 'noi_dung')
        }),
        ('Trạng thái hiển thị', {
            'fields': ('hien_thi',)
        }),
        ('Tùy chỉnh SEO (Xem trước kết quả tìm kiếm)', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_description', 'duong_dan_alias'),
            'description': 'Thiết lập các thẻ mô tả giúp khách hàng dễ dàng tìm thấy bài viết trên công cụ tìm kiếm như Google.'
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'anh_dai_dien' in form.changed_data and form.cleaned_data.get('anh_dai_dien'):
            webp = _to_webp(form.cleaned_data['anh_dai_dien'])
            if webp:
                obj.anh_dai_dien.save(webp.name, webp, save=False)
        super().save_model(request, obj, form, change)


@admin.register(DangKyTuVan)
class DangKyTuVanAdmin(admin.ModelAdmin):
    list_display = ('so_dien_thoai', 'tinh_thanh', 'ngay_dang_ky', 'da_lien_he')
    list_filter = ('da_lien_he', 'tinh_thanh')
    search_fields = ('so_dien_thoai', 'tinh_thanh')
    list_editable = ('da_lien_he',)
    readonly_fields = ('so_dien_thoai', 'tinh_thanh', 'ngay_dang_ky')
    actions = ['export_csv']

    def has_add_permission(self, request):
        return False

    @admin.action(description='⬇ Xuất danh sách đã chọn ra file Excel (CSV)')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f"khach_hang_tu_van_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['STT', 'Số điện thoại', 'Tỉnh/Thành phố', 'Ngày đăng ký', 'Đã liên hệ'])
        for i, obj in enumerate(queryset.order_by('-ngay_dang_ky'), 1):
            writer.writerow([
                i,
                obj.so_dien_thoai,
                obj.tinh_thanh,
                obj.ngay_dang_ky.strftime('%d/%m/%Y %H:%M'),
                'Có' if obj.da_lien_he else 'Chưa',
            ])
        return response
