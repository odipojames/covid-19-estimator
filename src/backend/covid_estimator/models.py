# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import HStoreField

from django.db import models

# Create your models here.
Period_Choices = (
    ("Days", "Days"),
    ("Weeks", "Weeks"),
    ("Months", "Months"),
)


class Region(models.Model):
    """region information"""

    name = models.CharField(max_length=50)
    avg_age = models.FloatField()
    avg_daily_income = models.FloatField()
    avg_daily_income_population = models.FloatField()

    def __str__(self):
        return self.name


class RegionData(models.Model):
    """class to store regions covid data"""

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    period_type = models.CharField(
        max_length=20, choices=Period_Choices, default="Days"
    )
    time_to_elapse = models.PositiveIntegerField()
    reported_cases = models.PositiveIntegerField()
    population = models.PositiveIntegerField()
    total_hosiptal_beds = models.PositiveIntegerField()


class Log(models.Model):
    """model to store request logs"""

    time_stamp = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
