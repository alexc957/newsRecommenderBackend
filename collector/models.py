

# Create your models here.
from django.db import models
from django.conf import settings
from datetime import date
from django.utils.timezone import now
# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    article = models.ForeignKey('articles.Article', related_name='vote',on_delete= models.CASCADE)
    liked = models.BooleanField(default=True)
    create_at = models.DateField(default = now())