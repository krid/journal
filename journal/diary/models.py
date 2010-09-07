from django.db import models
from django.contrib.auth.models import User

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
                                           null=True)
    reality = models.SmallIntegerField(choices=EXPECTATIONS_VS_REALITY)


class SummaryAndNotes(models.Model):
    """ Abstract mixin for models that have a summary and notes. """

    class Meta:
        abstract = True

    summary = models.CharField(max_length=100,
                               null=False,
                               blank=False)
    notes = models.TextField(null=True)


class Entry(SummaryAndNotes, Timestamped):
    """ Basic diary entry. """

    class Meta:
        ordering = ["created"]
        get_latest_by = "created"
        verbose_name_plural = "Entries"

    def __str__(self):
        return str(unicode(self))
    def __unicode__(self):
        return '{summary} - {created}'.format(summary=self.summary,
                                              created=self.created.strftime('%Y-%m-%d %H:%M'))

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

    mood = models.CharField(max_length=20,
                            null=False,
                            blank=False,
                            choices=MOODS)

    user = models.ForeignKey(User, null=False)

    media = models.ManyToManyField('Media')


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
        return '{type}: {summary} - {created}'.format(type=self.activity_type,
                                                      summary=self.summary,
                                                      created=self.created.strftime('%Y-%m-%d'))

    entry = models.ForeignKey(Entry)

    duration = models.PositiveIntegerField("duration in hours", null=True)

    private = models.BooleanField()

    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)

    def save(self, *args, **kwargs):
        self.activity_type = self.__class__.__name__
        super(Activity, self).save(*args, **kwargs)


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

    company = models.ManyToManyField(Person)


class DiningOut(Activity):
    """ Food, for money """

    class Meta:
        verbose_name_plural = "dining out"

    restaurant = models.CharField(max_length=100)

    link = models.URLField()

    company = models.ManyToManyField(Person)


class Media(Rateable, SummaryAndNotes, Timestamped):
    """ Media purchased or consumed.
    
    TODO: Consider having a many-to-many with Entry via a "through" that
    captures the relation -- purchased, consumed, started, finished, etc.
    """

    MEDIA_TYPES = (('Book', 'Book'),
                   ('Music', 'Music'),
                   ('Video', 'Video'),
                   ('Media', 'Media'),
                   )

    class Meta:
        #abstract = True
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
                             null=False,
                             blank=False)

    link = models.URLField(null=True)

    year = models.IntegerField(null=True,
                               help_text="Year of publication/release.")

    referred_by = models.ForeignKey(Person, null=True)

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
                              null=False,
                              blank=False)

    book_type = models.CharField(max_length=20,
                                 choices=BOOK_TYPES,
                                 null=False,
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
                              null=False,
                              blank=False)

    source = models.CharField(max_length=100,
                              null=True,
                              blank=False)

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
                                  null=False,
                                  blank=False)
