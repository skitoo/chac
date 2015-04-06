from django.db import models
from jsonfield import JSONField


class Sensor(models.Model):
    name = models.CharField(max_length=25)
    activated = models.BooleanField(default=False)
    type = models.CharField(max_length=10)
    meta = JSONField()
