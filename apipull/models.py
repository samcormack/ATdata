from django.db import models
from django.utils import timezone

class RTentry(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    id_no = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100)
    route_id = models.CharField(max_length=100)
    stop_seq = models.IntegerField()
    stop_id = models.CharField(max_length=20)
    stop_type = models.CharField(max_length=20)
    vehicle_id = models.CharField(max_length=20)
    delay = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.id_no
