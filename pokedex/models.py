from django.db import models


# Create your models here.
class Pokemon(models.Model):
    api_id = models.CharField(max_length=30)
    img = models.CharField(max_length=500, null=True)


class Equipe(models.Model):
    name = models.CharField(max_length=30)
    pokemons = models.ManyToManyField(Pokemon)

