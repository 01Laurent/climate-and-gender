from django.contrib.gis.db import models as gismodels


class HealthFacilities(gismodels.Model):
    name = gismodels.CharField(max_length=80, null=True)
    healthcare = gismodels.CharField(max_length=167, null=True)
    amenity = gismodels.CharField(max_length=80, null=True)
    operatorty = gismodels.CharField(max_length=80, null=True)
    geom = gismodels.MultiPointField(srid=4326)

    class Meta:
        """
        indexe the geom, fastening fetch time
        """
        indexes = [
                gismodels.Index(fields=["geom"], name="geom_index")
                ]

        def __str__(self):
            return self.name
