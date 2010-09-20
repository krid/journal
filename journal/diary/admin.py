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
"""
Admin fu for diary

Dirk Bergstrom, krid@otisbean.com
2010-07-05

@author: krid
"""

from django.contrib import admin

from journal.diary.models import BikeRide, SocialEvent, DiningOut, Entry, \
    Person, Video, Book, Music, Activity, Media, MedicalObservation, Consumable, \
    Period, Event

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


class MedicalObservationInline(admin.TabularInline):
    model = MedicalObservation
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
               ConsumableInline,
               MedicalObservationInline, ]
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

class ConsumableAdmin(admin.ModelAdmin):
    pass
admin.site.register(Consumable, ConsumableAdmin)

class MedicalObservationAdmin(admin.ModelAdmin):
    pass
admin.site.register(MedicalObservation, MedicalObservationAdmin)

admin.site.register(Event)
admin.site.register(Period)
