from django.contrib import admin

# Register your models here.
from .models import Track, ST, Song

admin.site.register(Track)
admin.site.register(ST)
admin.site.register(Song)