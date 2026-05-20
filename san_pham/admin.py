from django.contrib import admin
from .models import VideoProject, Article

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
    # Đã thêm trường tac_gia vào danh sách hiển thị và bộ lọc
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