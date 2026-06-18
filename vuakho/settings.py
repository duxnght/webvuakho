import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Nạp biến môi trường từ file .env (nếu tồn tại)
load_dotenv(BASE_DIR / '.env')


# ==============================================================================
# CẤU HÌNH MẶC ĐỊNH — DÀNH CHO CPANEL (PRODUCTION)
# ==============================================================================

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['vuakhotronsanshk.com.vn', 'www.vuakhotronsanshk.com.vn']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'san_pham',
    'django.contrib.sitemaps',
    'cloudinary',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vuakho.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vuakho.wsgi.application'


# Database MySQL cho cPanel (production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Ngôn ngữ và múi giờ Việt Nam
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


# Static & Media files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Cloudinary — chỉ kích hoạt khi có credentials
# cloudinary_storage KHÔNG thêm vào INSTALLED_APPS: package 0.3.0 override
# collectstatic bằng command dùng settings.STATICFILES_STORAGE đã bị xóa trong
# Django 6.0. MediaCloudinaryStorage vẫn hoạt động bình thường vì nó tự gọi
# cloudinary.config() từ CLOUDINARY_STORAGE khi khởi tạo instance.
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    STORAGES = {
        'default': {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }
else:
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# CKEditor — upload ảnh trong thân bài viết
# Ảnh được view tùy biến (san_pham.ckeditor_views) chuyển sang WebP rồi lưu qua
# storage mặc định (Cloudinary trên production), giống pipeline ảnh đại diện.
# ==============================================================================
CKEDITOR_UPLOAD_PATH = 'blog_content/'
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_IMAGE_BACKEND = None  # tự convert WebP, không cần backend tạo thumbnail

CKEDITOR_CONFIGS = {
    'default': {
        'language': 'vi',
        'skin': 'moono-lisa',
        'toolbar': 'SHK',
        'toolbar_SHK': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['TextColor', 'BGColor'],
            ['RemoveFormat', 'Source', 'Maximize'],
        ],
        # uploadimage: dán (Ctrl+V) / kéo-thả ảnh vào bài là tự upload luôn.
        'extraPlugins': 'uploadimage',
        # CKEditor 4.22 (getUploadUrl) nối "&responseType=json" vào
        # filebrowserUploadUrl mà KHÔNG kiểm tra dấu "?" -> URL bị hỏng -> 404.
        # Đặt thẳng uploadUrl/imageUploadUrl để plugin lấy nguyên URL (đường dẫn
        # cố định = reverse('ckeditor_upload')); view tự trả JSON nên vẫn parse được.
        'uploadUrl': '/ckeditor/upload/',
        'imageUploadUrl': '/ckeditor/upload/',
        # Ẩn nút "Duyệt máy chủ" (ảnh nằm trên Cloudinary, không liệt kê được).
        'filebrowserBrowseUrl': '',
        'height': 400,
        'width': '100%',
    }
}

DEPLOY_WEBHOOK_TOKEN = os.environ.get('DEPLOY_WEBHOOK_TOKEN', '')


# ==============================================================================
# Nếu file local_settings.py tồn tại (local) → đè các cấu hình production ở trên.
# Trên cPanel không có file đó → bỏ qua.
# ==============================================================================
try:
    from .local_settings import *
except ImportError:
    pass


# ==============================================================================
# HTTPS SECURITY HEADERS — chỉ kích hoạt khi DEBUG=False (production)
# Các giá trị này được đọc SAU khi local_settings.py đã ghi đè DEBUG,
# nên trên máy local (DEBUG=True) những dòng này sẽ không chạy.
# ==============================================================================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000          # 1 năm
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True            # Session cookie chỉ qua HTTPS
    CSRF_COOKIE_SECURE = True               # CSRF cookie chỉ qua HTTPS
