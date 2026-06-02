# Generated manually for TikTok support on VideoProject

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('san_pham', '0003_dangkytuvan'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoproject',
            name='nen_tang',
            field=models.CharField(
                choices=[('YOUTUBE', 'YouTube'), ('TIKTOK', 'TikTok')],
                default='YOUTUBE',
                max_length=10,
                verbose_name='Nền tảng video',
            ),
        ),
        migrations.AddField(
            model_name='videoproject',
            name='link_tiktok',
            field=models.URLField(
                blank=True,
                null=True,
                help_text='Dán link video TikTok đầy đủ (chọn khi nền tảng là TikTok). Vd: https://www.tiktok.com/@user/video/7123...',
                verbose_name='Đường dẫn TikTok',
            ),
        ),
        migrations.AddField(
            model_name='videoproject',
            name='anh_thumbnail',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='video_thumbs/',
                help_text='Bắt buộc cho TikTok. YouTube để trống sẽ tự lấy ảnh bìa.',
                verbose_name='Ảnh thumbnail',
            ),
        ),
        migrations.AddField(
            model_name='videoproject',
            name='thumbnail_url',
            field=models.URLField(
                blank=True,
                null=True,
                editable=False,
                verbose_name='Thumbnail tự động (TikTok)',
            ),
        ),
    ]
