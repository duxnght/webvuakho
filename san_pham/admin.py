import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from .models import VideoProject, Article, DangKyTuVan

admin.site.site_header = "Hệ thống Quản trị Vữa Khô Sông Hồng"
admin.site.site_title = "Admin Sông Hồng"
admin.site.index_title = "Bảng điều khiển"


@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'phan_loai', 'sap_ra_mat', 'ngay_tao')
    list_filter = ('phan_loai', 'sap_ra_mat')
    search_fields = ('tieu_de',)


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
        response = HttpResponse(
            content_type='text/csv; charset=utf-8-sig'  # utf-8-sig = BOM, Excel đọc được tiếng Việt
        )
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
