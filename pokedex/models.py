from django.db import models


# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=30)
    img_default = models.CharField(max_length=500, null=True)
    img_shiny = models.CharField(max_length=500, null=True)
    objects = models.Manager()
