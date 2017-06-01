from django.db import models

# Create your models here.

class Song(models.Model):
    songID = models.CharField(max_length=30)
    hashcode = models.IntegerField()

class Track(models.Model):
    year = models.IntegerField()
    trackID = models.CharField(max_length=30)
    artist = models.CharField(max_length=150, null=True)
    name = models.CharField(max_length=150)

class ST(models.Model):
    songID = models.CharField(max_length=30)
    trackID = models.CharField(max_length=30)