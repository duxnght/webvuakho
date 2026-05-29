from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return [
            ('home_page',     1.0, 'weekly'),
            ('blog_page',     0.8, 'weekly'),
            ('tai_lieu_page', 0.7, 'monthly'),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class ArticleSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Article.objects.filter(hien_thi=True)

    def lastmod(self, obj):
        return obj.ngay_dang

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.duong_dan_alias})
