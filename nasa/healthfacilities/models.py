from django.contrib.gis.db import models


class HealthFacilities(models.Model):
    name = models.CharField(max_length=80)
    healthcare = models.CharField(max_length=167)
    amenity = models.CharField(max_length=80)
    operatorty = models.CharField(max_length=80)
    geom = models.PointField(srid=4326)

    def __str__(self):
        return self.name
