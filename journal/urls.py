from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse

from journal.diary.models import BikeRide, SocialEvent, DiningOut, Entry, \
    Person, Video, Book, Music, Activity, Media

admin.autodiscover()

databrowse.site.register(Entry)
databrowse.site.register(Activity)
databrowse.site.register(Media)
databrowse.site.register(BikeRide)
#databrowse.site.register()

urlpatterns = patterns('',
    # Example:
    # (r'^journal/', include('journal.foo.urls')),

    (r'^browse/(.*)', databrowse.site.root),

    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
