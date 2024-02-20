from django.db import models

# Create your models here.
class Repository(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()
    link = models.URLField()
    website = models.CharField(max_length=200)