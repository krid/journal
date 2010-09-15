import os, sys
sys.path.append('/usr/lib/wsgi')
os.environ['DJANGO_SETTINGS_MODULE'] = 'journal.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()