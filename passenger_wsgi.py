import os
import sys

INTERP = '/home/nhkeos0p/virtualenv/webvuakho/3.12/bin/python3'
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '/home/nhkeos0p/webvuakho')

os.environ['DJANGO_SETTINGS_MODULE'] = 'vuakho.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
