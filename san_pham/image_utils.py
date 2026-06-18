import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image as PilImage


def to_webp(uploaded_file, quality=85):
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
