from django.db import models
from django.conf import settings
from articles.models import Article
# Create your models here.

class Recommendation(models.Model):
    score = models.FloatField()
    user = models.ForeignKey( settings.AUTH_USER_MODEL, null = True, on_delete= models.CASCADE) 
    article = models.ForeignKey(Article, null =True, on_delete = models.CASCADE)
    recommended = models.BooleanField(default=False)
