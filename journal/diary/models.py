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

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm

# The Timeline package doesn't like open-ended date ranges, so we bookend...
YEAR_ZERO = '1900-01-01'
YEAR_INFINITY = '2100-01-01'
INDETERMINATE_TIME = "~"

class Timestamped(models.Model):
    """ Abstract mixin for models that have created & modified times. """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True,
                                   blank=False,
                                   db_index=True)
    modified = models.DateTimeField(auto_now_add=True,
                                    auto_now=True,
                                    blank=False,
                                    db_index=True)


class Rateable(models.Model):
    """ Abstract mixin for models that support expectations-vs-reality
    star ratings. """

    class Meta:
        abstract = True

    EXPECTATIONS_VS_REALITY = (
        (5, 'Excellent'),
        (4, 'Great'),
        (3, 'Good'),
        (2, 'OK'),
        (1, 'Bad'),
        (0, 'Awful'),
    )

    expectation = models.SmallIntegerField(choices=EXPECTATIONS_VS_REALITY,
                                           blank=True,
                                           null=True)
    reality = models.SmallIntegerField(choices=EXPECTATIONS_VS_REALITY)


class SummaryAndNotes(models.Model):
    """ Abstract mixin for models that have a summary and notes. """

    class Meta:
        abstract = True

    summary = models.CharField(max_length=100,
                               blank=False)
    notes = models.TextField(blank=True)


class Entry(SummaryAndNotes, Timestamped):
    """ Basic diary entry. """

    class Meta:
        ordering = ["-date"]
        get_latest_by = "date"
        verbose_name_plural = "Entries"

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{summary} - {date}'.format(summary=self.summary,
                                              date=self.date.strftime('%Y-%m-%d'))

    MOODS = (
       ('very-happy', 'Very Happy'),
       ('happy', 'Happy'),
       ('good', 'Good'),
       ('ok', 'OK'),
       ('down', 'Down'),
       ('frustrated', 'Frustrated'),
       ('angry', 'Angry'),
       ('depressed', 'Depressed'),
       ('sick', 'Sick'),
    )

    date = models.DateField(blank=False,
                            db_index=True)

    mood = models.CharField(max_length=20,
                            blank=False,
                            choices=MOODS)

    user = models.ForeignKey(User)

    media = models.ManyToManyField('Media')

    consumables = models.ManyToManyField('Consumable')

    def as_timeline_dict(self):
        return dict(start=self.date.strftime('%Y-%m-%d'),
                    durationEvent=False,
                    title=self.summary,
                    classname=self.__class__.__name__,
                    id=str(self.pk),
                    )


class Person(SummaryAndNotes, Timestamped):
    """ A person or group of people. """

    class Meta:
        ordering = ["created"]
        get_latest_by = "created"
        verbose_name_plural = "People"

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return "{0}".format(self.name)

    RELATIONS = (
        ('relative', 'Relative'),
        ('friend', 'Friend'),
        ('co-worker', 'CoW-orker'),
        ('acquaintance', 'Acquaintance'),
        ('stranger', 'Stranger'),
    )

    name = models.CharField(max_length=100)

    relation = models.CharField(max_length=20, choices=RELATIONS)

    met = models.DateField(db_index=True)

    def as_timeline_dict(self):
        return dict(start=self.met.strftime('%Y-%m-%d'),
                    durationEvent=False,
                    title=self.name,
                    classname=self.__class__.__name__,
                    id=str(self.pk),
                    )


class Activity(Rateable, SummaryAndNotes, Timestamped):
    """ Base class for an activity you took part in. """

    ACTIVITY_TYPES = (('BikeRide', 'BikeRide'),
                      ('SocialEvent', 'SocialEvent'),
                      ('DiningOut', 'DiningOut'),
                      ('Activity', 'Activity'),
                      )

    class Meta:
        #abstract = True
        ordering = ["created"]
        get_latest_by = "created"
        verbose_name_plural = 'activities'

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{type}: {summary} - {date}'.format(type=self.activity_type,
                                                   summary=self.summary,
                                                   date=self.entry.date.strftime('%Y-%m-%d'))
    entry = models.ForeignKey(Entry)

    duration = models.PositiveIntegerField("duration in hours",
                                           blank=True, null=True)

    private = models.BooleanField()

    activity_type = models.CharField(max_length=15, choices=ACTIVITY_TYPES)

    def save(self, *args, **kwargs):
        self.activity_type = self.__class__.__name__
        super(Activity, self).save(*args, **kwargs)

    def as_timeline_dict(self):
        return dict(start=self.entry.date.strftime('%Y-%m-%d'),
                    durationEvent=False,
                    title='{type}: {summary}'.format(type=self.activity_type,
                                                     summary=self.summary),
                    classname=self.activity_type,
                    id=str(self.pk),
                    )


class BikeRide(Activity):
    """ A bicycle ride. """

    class Meta:
        ordering = ["created"]
        get_latest_by = "created"

    distance = models.PositiveIntegerField("distance in miles")

    average_speed = models.DecimalField("average speed in mph",
                                        decimal_places=1,
                                        max_digits=3)

    climbing = models.PositiveIntegerField("climbing in feet")

    solo = models.BooleanField()


class SocialEvent(Activity):
    """ Visit, meeting, gathering or other interaction with people. """

    company = models.ManyToManyField(Person, blank=True)


class DiningOut(Activity):
    """ Food, for money """

    class Meta:
        verbose_name_plural = "dining out"

    restaurant = models.CharField(max_length=100)

    where = models.CharField(max_length=200,
                             blank=True)

    link = models.URLField(blank=True)

    company = models.ManyToManyField(Person, blank=True)

    consumables = models.ManyToManyField('Consumable', blank=True)


class Consumable(SummaryAndNotes, Rateable, Timestamped):
    """ Liquor, beer, wine, chocolate and other yummy foodstuffs. """

    CONSUMABLE_TYPES = (('Liquor', 'Liquor'),
                        ('Wine', 'Wine'),
                        ('Beer', 'Beer'),
                        ('Drugs', 'Drugs'),
                        ('Chocolate', 'Chocolate'),
                        ('Candy', 'Candy'),
                        ('Food', 'Food'),
                        )

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{type}: "{title}"'.format(type=self.consumable_type,
                                                  title=self.name)
    name = models.CharField(max_length=100)

    where = models.CharField(max_length=200, blank=True)

    link = models.URLField(blank=True)

    referred_by = models.ForeignKey(Person, blank=True, null=True)

    consumable_type = models.CharField(max_length=10, choices=CONSUMABLE_TYPES)


class Media(SummaryAndNotes, Rateable, Timestamped):
    """ Media purchased or consumed.
    
    TODO: Consider having a many-to-many with Entry via a "through" that
    captures the relation -- purchased, consumed, started, finished, etc.
    Could use the same model (or a clone) to handle Consumables.  This
    would require some snazzy UI to make it easy to do the association -- or
    maybe the admin UI handles this already?  Hmm, it also gets messy if you
    want to both 'purchase' and 'consume' something at the same time.  Maybe
    this is over-thinking it...
    """

    MEDIA_TYPES = (('Book', 'Book'),
                   ('Music', 'Music'),
                   ('Video', 'Video'),
                   ('Media', 'Media'),
                   )

    class Meta:
        ordering = ["created"]
        get_latest_by = "created"
        verbose_name_plural = 'media'

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{type}: "{title}" {year}'.format(type=self.media_type,
                                                  title=self.title,
                                                  year=self.year)

    title = models.CharField(max_length=100,
                             blank=False)

    link = models.URLField(blank=True)

    year = models.IntegerField(blank=True,
                               help_text="Year of publication/release.")

    referred_by = models.ForeignKey(Person,
                                    blank=True, null=True)

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)

    def save(self, *args, **kwargs):
        self.media_type = self.__class__.__name__
        super(Media, self).save(*args, **kwargs)


class Book(Media):
    """ A book, comic, graphic novel, etc. """

    BOOK_TYPES = (
        ('novel', 'Novel'),
        ('graphic-novel', 'Graphic Novel'),
        ('comic', 'Comic'),
        ('magazine', 'Magazine'),
    )

    GENRES = (
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('superhero', 'Superhero'),
        ('historical', 'Historical Fiction'),
        ('experimental', 'Experimental'),
        ('contemporary', 'Contemporary'),
        ('non-fiction', 'non-fiction'),
    )

    class Meta:
        verbose_name = "book"

    author = models.CharField(max_length=100,
                              blank=False)

    book_type = models.CharField(max_length=20,
                                 choices=BOOK_TYPES,
                                 blank=False)

    genre = models.CharField(max_length=20,
                             choices=GENRES)


class Music(Media):
    """ Album, song, symphony, etc. """

    class Meta:
        verbose_name = "music"
        verbose_name_plural = "music"

    GENRES = (
        ('metal', 'Metal'),
        ('indie', 'Indie Rock'),
        ('post-rock', 'Post Rock'),
        ('classical', 'Classical'),
    )


    artist = models.CharField(max_length=100,
                              blank=False)

    source = models.CharField(max_length=100,
                              blank=True)

    genre = models.CharField(max_length=20,
                             choices=GENRES)


class Video(Media):
    """ Movie, TV show, etc. """

    class Meta:
        verbose_name = "video"

    VIDEO_TYPES = (
        ('movie', 'Movie'),
        ('tv-show', 'TV Show'),
        ('episode', 'Episode'),
    )

    video_type = models.CharField(max_length=20,
                                  choices=VIDEO_TYPES,
                                  blank=False)


class MedicalObservation(SummaryAndNotes, Timestamped):
    """ What's going on with your body or mind. """

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{summary} - {date}'.format(summary=self.summary,
                                           date=self.entry.date.strftime('%Y-%m-%d'))

    entry = models.ForeignKey(Entry)

    def as_timeline_dict(self):
        return dict(start=self.entry.date.strftime('%Y-%m-%d'),
                    durationEvent=False,
                    title=self.summary,
                    classname=self.__class__.__name__,
                    id=str(self.pk),
                    )


class DateWithOptionalTimeMixin(object):
    """ Provides a method to emit date or date + time depending on the fields
    populated.
    """

    def get_date_time_string(self, field=None):
        # If no field given do "date" and "time", otherwise "<field>_date"...
        field_name = field and '{0}_'.format(field) or ''
        timeval = getattr(self, '{0}time'.format(field_name))
        dateval = getattr(self, '{0}date'.format(field_name))
        retval = dateval and dateval.strftime('%Y-%m-%d') or ''
        if timeval:
            retval = '{0}{1}{2}'.format(retval, retval and ' ' or '',
                                        timeval.strftime('%H:%M'))
            # FIXME Think about timezones...
        return retval


class Event(SummaryAndNotes, Timestamped, DateWithOptionalTimeMixin):
    """ A significant life event.
    
    TODO Might be nice to have an optional type attribute, but concert is the
    only type I can think of right now.
    """

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{summary}: {date}'.format(summary=self.summary,
            date=self.get_date_time_string())

    date = models.DateField(blank=False,
                            db_index=True)

    time = models.TimeField(blank=True,
                            null=True,
                            db_index=False)

    def as_timeline_dict(self):
        return dict(id=str(self.pk),
                    start=self.get_date_time_string(),
                    durationEvent=False,
                    title=self.summary,
                    classname='Event',
                    )


class Period(SummaryAndNotes, Timestamped, DateWithOptionalTimeMixin):
    """ A period of time. """

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{summary}: {start} -> {end}'.format(summary=self.summary,
            start=self.get_date_time_string('start'),
            end=self.get_date_time_string('end'))

    start_date = models.DateField(blank=True, null=True, db_index=True)
    start_time = models.TimeField(null=True, blank=True)

    latest_start_date = models.DateField(null=True, blank=True)
    latest_start_time = models.TimeField(null=True, blank=True)

    earliest_end_date = models.DateField(null=True, blank=True)
    earliest_end_time = models.TimeField(null=True, blank=True)

    end_date = models.DateField(blank=True, null=True, db_index=True)
    end_time = models.TimeField(null=True, blank=True)

    def as_timeline_dict(self):
        caption = u"{0}: {1} \u21D2 {2}".format(self.summary,
                                     self.start_date or INDETERMINATE_TIME,
                                     self.end_date or INDETERMINATE_TIME)
        retval = dict(id=str(self.pk),
                      start=self.get_date_time_string('start') or YEAR_ZERO,
                      end=self.get_date_time_string('end') or YEAR_INFINITY,
                      durationEvent=True,
                      title=self.summary,
                      caption=caption, # TODO replace with tooltip?
                      classname=self.__class__.__name__,
                      )
        if self.latest_start_date or self.latest_start_time:
            retval['latestStart'] = self.get_date_time_string('latest_start')
        if self.earliest_end_date or self.earliest_end_time:
            retval['earliestEnd'] = self.get_date_time_string('earliest_end')
        return retval


class EntryForm(ModelForm):
    class Meta:
        model = Entry


class PersonForm(ModelForm):
    class Meta:
        model = Person


class ActivityForm(ModelForm):
    class Meta:
        model = Activity


class BikeRideForm(ModelForm):
    class Meta:
        model = BikeRide


class SocialEventForm(ModelForm):
    class Meta:
        model = SocialEvent


class DiningOutForm(ModelForm):
    class Meta:
        model = DiningOut


class ConsumableForm(ModelForm):
    class Meta:
        model = Consumable


class MediaForm(ModelForm):
    class Meta:
        model = Media


class BookForm(ModelForm):
    class Meta:
        model = Book


class MusicForm(ModelForm):
    class Meta:
        model = Music


class VideoForm(ModelForm):
    class Meta:
        model = Video


class MedicalObservationForm(ModelForm):
    class Meta:
        model = MedicalObservation


class EventForm(ModelForm):
    class Meta:
        model = Event


class PeriodForm(ModelForm):
    class Meta:
        model = Period
