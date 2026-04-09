from django.db import models

class temperature(models.Model):
    #myid int
    #sensor_id int
    #temperature float
    #humidity float
    #timestamp datatime
    myid = models.AutoField(primary_key=True)
    sensor_id = models.IntegerField(blank=False, null=False)
    temperature= models.IntegerField(blank=False, null=False)
    humidity = models.FloatField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"ID:{self.myid}, Sensor ID: {self.sensor_id}, Temperature: {self.temperature}, Humidity: {self.humidity}, Timestamp: {self.timestamp}"