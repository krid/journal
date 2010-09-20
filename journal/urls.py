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
from django.contrib import databrowse
from django.conf import settings

from journal.diary.models import BikeRide, SocialEvent, DiningOut, Entry, \
    Person, Video, Book, Music, Activity, Media
from journal.diary import views

admin.autodiscover()

databrowse.site.register(Entry)
databrowse.site.register(Activity)
databrowse.site.register(Media)
databrowse.site.register(BikeRide)
#databrowse.site.register()

urlpatterns = patterns('',
    # Example:
    # (r'^journal/', include('journal.foo.urls')),

    (r'^timeline/(?P<line_type>[^/]+)/', views.timeline),
    (r'^timeline_json/(?P<line_type>[^/]+)/', views.timeline_json),

    (r'^browse/(.*)', databrowse.site.root),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # This is here so we can have a url mapping in templates 
    url(r'^static$', views.static_url, name='static'),
)
print settings.DEVELOPMENT
if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

