import re
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# LUỒNG VIDEO DỰ ÁN
class VideoProject(models.Model):
    SERIES_CHOICES = [
        ('M7.5', 'M7.5 SERIES'),
        ('NANO', 'NANO SERIES'),
        ('JUMBO', 'JUMBO SERIES'),
    ]
    NEN_TANG_CHOICES = [
        ('YOUTUBE', 'YouTube'),
        ('TIKTOK', 'TikTok'),
    ]

    tieu_de = models.CharField(max_length=200, verbose_name="Tên dự án")
    phan_loai = models.CharField(max_length=20, choices=SERIES_CHOICES, default='M7.5', verbose_name="Dòng sản phẩm")
    nen_tang = models.CharField(max_length=10, choices=NEN_TANG_CHOICES, default='YOUTUBE', verbose_name="Nền tảng video")
    link_youtube = models.URLField(blank=True, null=True, verbose_name="Đường dẫn YouTube", help_text="Dán link YouTube (chọn khi nền tảng là YouTube). Vd: https://www.youtube.com/watch?v=...")
    link_tiktok = models.URLField(blank=True, null=True, verbose_name="Đường dẫn TikTok", help_text="Dán link video TikTok đầy đủ (chọn khi nền tảng là TikTok). Vd: https://www.tiktok.com/@user/video/7123...")
    anh_thumbnail = models.ImageField(upload_to='video_thumbs/', blank=True, null=True, verbose_name="Ảnh thumbnail", help_text="Bắt buộc cho TikTok. YouTube để trống sẽ tự lấy ảnh bìa.")
    thumbnail_url = models.URLField(blank=True, null=True, editable=False, verbose_name="Thumbnail tự động (TikTok)")
    sap_ra_mat = models.BooleanField(default=False, verbose_name="Dự án sắp ra mắt (Chưa có video)")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Video Phóng sự"
        verbose_name_plural = "Quản lý Video Phóng sự"
        ordering = ['-ngay_tao']

    def __str__(self):
        return self.tieu_de

    @property
    def youtube_id(self):
        if not self.link_youtube:
            return ''
        m = re.search(r'(?:youtu\.be/|/v/|/embed/|watch\?v=|&v=)([^#&?]{11})', self.link_youtube)
        return m.group(1) if m else ''

    @property
    def tiktok_id(self):
        if not self.link_tiktok:
            return ''
        m = re.search(r'/video/(\d+)', self.link_tiktok)
        return m.group(1) if m else ''

    @property
    def thumb_url(self):
        """Trả về URL ảnh thumbnail phù hợp theo nền tảng."""
        if self.anh_thumbnail:
            return self.anh_thumbnail.url
        if self.thumbnail_url:
            return self.thumbnail_url
        if self.youtube_id:
            return f'https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg'
        return ''

# LUỒNG BÀI VIẾT BLOG
class Article(models.Model):
    tieu_de = models.CharField(max_length=255, verbose_name="Tiêu đề bài viết")
    
    # TRƯỜNG MỚI: Cho phép điền tên tác giả
    tac_gia = models.CharField(max_length=100, default="Ban Giám Đốc", verbose_name="Tác giả", help_text="Tên người viết bài")
    
    anh_dai_dien = models.ImageField(upload_to='blog_images/', verbose_name="Ảnh bài viết")
    mo_ta_ngan = models.TextField(max_length=500, verbose_name="Mô tả ngắn")
    noi_dung = RichTextField(verbose_name="Nội dung bài viết")
    
    hien_thi = models.BooleanField(default=True, verbose_name="Hiện bài viết")
    ngay_dang = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    
    seo_title = models.CharField(max_length=70, blank=True, verbose_name="Tiêu đề trang (SEO)", help_text="Tối đa 70 ký tự")
    seo_description = models.TextField(max_length=320, blank=True, verbose_name="Thẻ mô tả (SEO)", help_text="Tối đa 320 ký tự")
    duong_dan_alias = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Đường dẫn / Alias", help_text="Để trống hệ thống sẽ tự tạo từ Tiêu đề")

    class Meta:
        verbose_name = "Bài viết Blog"
        verbose_name_plural = "Quản lý Bài viết Blog"
        ordering = ['-ngay_dang']

    def __str__(self):
        return self.tieu_de

    def save(self, *args, **kwargs):
        if not self.duong_dan_alias:
            base_slug = slugify(self.tieu_de)
            slug = base_slug
            counter = 1
            while Article.objects.filter(duong_dan_alias=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.duong_dan_alias = slug
        super().save(*args, **kwargs)


class DangKyTuVan(models.Model):
    so_dien_thoai = models.CharField(max_length=20, verbose_name="Số điện thoại")
    tinh_thanh = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    ngay_dang_ky = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")
    da_lien_he = models.BooleanField(default=False, verbose_name="Đã liên hệ")

    class Meta:
        verbose_name = "Đăng ký tư vấn"
        verbose_name_plural = "Quản lý Đăng ký tư vấn"
        ordering = ['-ngay_dang_ky']

    def __str__(self):
        return f"{self.so_dien_thoai} – {self.tinh_thanh}"