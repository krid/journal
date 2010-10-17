# Journal
# Copyright (C) 2010, Dirk Bergstrom, dirk@otisbean.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from journal.diary import views

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^journal/', include('journal.foo.urls')),

    (r'^timeline/(?P<line_type>[^/]+)/', views.timeline),
    (r'^timeline_json/(?P<line_type>[^/]+)/', views.timeline_json),

    # Render details for an info bubble
    (r'^details/(?P<model_type>[^/]+)/(?P<pk>[0-9]+)/', views.model_details),

    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # These are here so we can have url mapping in templates.  Don't call them...
    url(r'^static$', lambda request: 1, name='static'),
    url(r'^$', lambda request: 1, name='base'),
)

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

