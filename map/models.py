from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    states = models.ManyToManyField('State', through='Trip')
    trips_per_page = models.SmallIntegerField(
        default=10,
        validators=[
            MinValueValidator(5),
            MaxValueValidator(100)
        ]
    )

class State(models.Model):

    REGIONS = [
        ('W', 'West'),
        ('MW', 'Midwest'),
        ('NE', 'Northeast'),
        ('SW', 'Southwest'),
        ('SE', 'Southeast')
    ]

    name = models.CharField(max_length=14)
    code = models.CharField(max_length=2)
    region = models.CharField(max_length=2, choices=REGIONS)

    class Meta:
       ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Trip(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='trips')
    location = models.CharField(max_length=50)
    state = models.ForeignKey('State', on_delete=models.RESTRICT, related_name='trips')
    description = models.TextField(blank=True, null=True)
    date1 = models.DateField(blank=True, null=True)
    date2 = models.DateField(blank=True, null=True)

    class Meta:
       ordering = ['-date1', '-pk']

    def serialize(self):
        return {
            "id": self.pk,
            "location": self.location,
            "state": self.state.code,
            "description": self.description,
            "date1": self.date1,
            "date2": self.date2
        }

    def __str__(self):
        return f"{self.location}, {self.state}"


class Achievement(models.Model):
    slug = models.SlugField(max_length=15)
    icon = models.SlugField(max_length=20)
    color = models.SlugField(max_length=10)
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} ({self.slug})"
