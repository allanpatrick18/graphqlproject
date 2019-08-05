from django.db import models

# Create your models here.

from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Gender(ChoiceEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNIDENTIFIED = "UNIDENTIFIED"


class User(models.Model):
    gender = models.CharField(max_length=100,
                                   choices=Gender.choices(),
                                   default=Gender.UNIDENTIFIED.value)

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.email


class Website(models.Model):
    url = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.url


class Visit(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Stats (models.Model):
    users_count = models.IntegerField()
    websites_count = models.IntegerField()
    visits_count = models.IntegerField()
    users = models.ManyToManyField(User)
    websites = models.ManyToManyField(Website)
    visits = models.ManyToManyField(Visit)