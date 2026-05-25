import os
import sys
import pymysql

pymysql.install_as_MySQLdb()

sys.path.insert(0, '/home/nhkeos0p/webvuakho')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vuakho.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
