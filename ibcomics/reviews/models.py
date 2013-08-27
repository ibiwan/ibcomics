from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Reviewer(models.Model):
    user = models.OneToOneField(User) 
    name = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Review(models.Model):
    comic = models.ForeignKey(Comic)
    reviewer = models.ForeignKey(Reviewer)
    review_text = models.CharField(max_length=2000)
    stars = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date reviewed')
    def __unicode__(self):
        return str(self.reviewer) + ": " + str(self.stars)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

class Comic(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    def average_rating(self):
        accum = 0.0
        for review in self.review_set.all:
            accum += review.stars
        return accum / float(len(self.review_set.all))