"""
Admin fu for diary

Dirk Bergstrom, krid@otisbean.com
2010-07-05

@author: krid
"""

from django.contrib import admin

from journal.diary.models import BikeRide, SocialEvent, DiningOut, Entry, \
    Person, Video, Book, Music, Activity, Media

class ConsumableInline(admin.TabularInline):
    model = Entry.consumables.through
    extra = 1


class MediaInline(admin.TabularInline):
    model = Entry.media.through
    extra = 1


class BikeRideInline(admin.TabularInline):
    model = BikeRide
    #fields = ('summary', 'reality', 'distance', 'average_speed', 'climbing', 'solo')
    extra = 1


class SocialEventInline(admin.TabularInline):
    model = SocialEvent
    #fields = ('summary', 'reality', 'private',)
    extra = 1


class DiningOutInline(admin.TabularInline):
    model = DiningOut
    #fields = ('summary', 'reality', 'restaurant',)
    extra = 1


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('date', 'summary', 'notes', 'mood', 'user')
    list_display = ('date', 'summary', 'mood', 'user', 'modified')
    list_editable = ('summary', 'mood')
    list_display_links = ('date',)
    exclude = ('media',)
    date_hierarchy = 'date'
    search_fields = ('summary',)
    list_filter = ('mood',)
    inlines = [ActivityInline,
               BikeRideInline,
               SocialEventInline,
               DiningOutInline,
               MediaInline,
               ConsumableInline, ]
admin.site.register(Entry, EntryAdmin)


class BikeRideAdmin(admin.ModelAdmin):
    list_display = ('summary', 'reality', 'distance', 'average_speed', 'climbing', 'solo')
admin.site.register(BikeRide, BikeRideAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)


class SocialEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(SocialEvent, SocialEventAdmin)


class DiningOutAdmin(admin.ModelAdmin):
    pass
admin.site.register(DiningOut, DiningOutAdmin)


class VideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Video, VideoAdmin)


class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)


class MusicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Music, MusicAdmin)
