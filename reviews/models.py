from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Comic(models.Model):
    RATING_UNRATED = 'un'
    RATING_G       = 'g'
    RATING_PG      = 'pg'
    RATING_PG_13   = 'pg13'
    RATING_R       = 'r'
    RATING_NC_17   = 'nc17'
    MPAA_RATING_CHOICES = (
        (RATING_UNRATED, '(Unrated)'),
        (RATING_G,       'G'), 
        (RATING_PG,      'PG'), 
        (RATING_PG_13,   'PG-13'), 
        (RATING_R,       'R'), 
        (RATING_NC_17,   'NC-17'),
    ) 
    @classmethod
    def mpaa_choices(cls):
        return [{'db':db,'readable':readable} for (db, readable) in cls.MPAA_RATING_CHOICES]

    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    mpaa_rating = models.CharField(
        max_length=4, 
        choices=MPAA_RATING_CHOICES,
        default=RATING_UNRATED)
    def __unicode__(self):
        return self.name
    def average_rating(self):
        n = len(self.review_set.all())
        return sum([r.stars for r in self.review_set.all()]) / float(n) if n > 0 else 0.0
    def mpaa_rating_db(self):
        return self.mpaa_rating
    def mpaa_rating_readable(self):
        return {key:val for (key,val) in Comic.MPAA_RATING_CHOICES}[self.mpaa_rating]
    def tag_string(self):
        tagset = self.comictag_set.extra(order_by=['tag_text'])
        return " ".join([t.tag_text for t in tagset])

class Reviewer(models.Model):
    user = models.OneToOneField(User) 
    name = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    def reviews_by_comic(self):
        return self.review_set.extra(order_by=['comic__name'])

class Review(models.Model):
    comic = models.ForeignKey(Comic)
    reviewer = models.ForeignKey(Reviewer)
    review_text = models.CharField(max_length=2000)
    stars = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date reviewed')
    def __unicode__(self):
        return str(self.reviewer) + ": " + str(self.stars)
    def summary(self):
        maxlen = 60
        t = self.review_text.strip()
        if len(t) > maxlen:
            return t[:maxlen-3] + '...'
        else:
            return t

class ComicTag(models.Model):
    comic = models.ForeignKey(Comic)
    tag_text = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.tag_text)

class ReviewFlag(models.Model):
    review = models.ForeignKey(Review)
    ip_addr = models.IPAddressField()
    def __unicode__(self):
        return str(self.ip_addr)
