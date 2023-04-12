from django.core.exceptions import ValidationError
from django.db import models
#from rest_framework.exceptions import ValidationError

import uuid

class Brand(models.Model):

    #id = models.IntegerField(primary_key=True)
    brand_fondator = models.CharField(max_length=400)
    brand_name = models.CharField(max_length=400)
    brand_rank = models.CharField(max_length=400)
    nr_models = models.IntegerField()



class Dress(models.Model):


    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    color = models.CharField(max_length=400)
    model_wearing = models.CharField(max_length=400)
    price = models.IntegerField(default=90)
    brand_id = models.ForeignKey(Brand, related_name="dresses", on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.description


class RedCarpetPresentation(models.Model):

    #id = models.IntegerField(primary_key=True)
    holder = models.CharField(max_length=200)
    city_name = models.CharField(max_length=200)
    special_guest = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    nr_guests = models.IntegerField()
    dresses = models.ManyToManyField('Dress', through='ShowEvent')

class ShowEvent(models.Model):
    #id = models.IntegerField(primary_key=True)
    pieces = models.IntegerField()
    show_date = models.CharField(max_length=200)
    show_popularity = models.IntegerField()
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    presentation = models.ForeignKey(RedCarpetPresentation, on_delete=models.CASCADE)


