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


class RegionData(models.Model):
    """class to store regions data"""

    region = HStoreField()
    period_type = models.CharField(max_length=20, choices=Period_Choices)
    reported_cases = models.PositiveIntegerField()
    pupulation = models.PositiveIntegerField()
    total_hosiptal_beds = models.PositiveIntegerField()
