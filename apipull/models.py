from django.db import models
from django.utils import timezone

class RTentry(models.Model):
    call = models.ForeignKey('CallRecord',on_delete=models.PROTECT,null=True)
    id_no = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100)
    route_id = models.ForeignKey('Route',on_delete=models.PROTECT,null=True)
    stop_seq = models.IntegerField()
    stop_id = models.ForeignKey('Stop',on_delete=models.PROTECT,null=True)
    stop_type = models.CharField(max_length=20)
    vehicle_id = models.CharField(max_length=20)
    delay = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.id_no

class CallRecord(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    connected = models.BooleanField(default=False)
    http_status = models.CharField(max_length=5,default='')
    json_status = models.CharField(max_length=20,default='')

    def __str__(self):
        return ['Time of call: ',self.timestamp,'\nHttp status: ',self.http_status,
        '\nJSON status: ',self.json_status]

class Route(models.Model):
    route_id = models.CharField(max_length=100,primary_key=True)
    agency_id = models.CharField(max_length=20)
    route_short_name = models.CharField(max_length=20)
    route_long_name = models.CharField(max_length=100)
    route_type = models.CharField(max_length=1)

    def __str__(self):
        return self.route_short_name

class Stop(models.Model):
    stop_id = models.CharField(max_length=10,primary_key=True)
    stop_lat = models.DecimalField(max_digits=10,decimal_places=6)
    stop_lon = models.DecimalField(max_digits=10,decimal_places=6)
    location_type = models.CharField(max_length=1)
    stop_code = models.CharField(max_length=10)
    stop_name = models.CharField(max_length=100)
    def __str__(self):
        return self.stop_name
