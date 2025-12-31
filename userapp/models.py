from django.db import models

# Create your models here.



from django.db import models

class GPS(models.Model):
    unit_no = models.CharField(max_length=50, null=True, blank=True)
    vehicle_no = models.CharField(max_length=50, null=True, blank=True)
    location_type = models.CharField(max_length=50, null=True, blank=True)

    track_time = models.DateTimeField(null=True, blank=True)
    direction_in_degree = models.FloatField(null=True, blank=True)
    satellite = models.IntegerField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)

    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    x_acceleration = models.FloatField(null=True, blank=True)
    y_acceleration = models.FloatField(null=True, blank=True)
    z_acceleration = models.FloatField(null=True, blank=True)
    tilt = models.FloatField(null=True, blank=True)
    impact = models.FloatField(null=True, blank=True)

    fuel_consumption = models.FloatField(null=True, blank=True)
    balance_fuel = models.FloatField(null=True, blank=True)

    hd_status = models.CharField(max_length=20, null=True, blank=True)
    hd_size = models.FloatField(null=True, blank=True)
    hd_balance = models.FloatField(null=True, blank=True)

    ibutton1 = models.CharField(max_length=50, null=True, blank=True)
    message_type = models.CharField(max_length=50, null=True, blank=True)
    ignition = models.BooleanField(default=False)
    gsm_signal = models.IntegerField(null=True, blank=True)
    polling_mode = models.CharField(max_length=50, null=True, blank=True)

    ha = models.FloatField(null=True, blank=True)
    hb = models.FloatField(null=True, blank=True)
    panic = models.BooleanField(default=False)
    fuel_bar = models.FloatField(null=True, blank=True)
    over_speed = models.BooleanField(default=False)
    analog = models.FloatField(null=True, blank=True)
    seat_belt = models.BooleanField(default=False)

    prev_value = models.FloatField(null=True, blank=True)
    ec = models.CharField(max_length=50, null=True, blank=True)
    tp = models.CharField(max_length=50, null=True, blank=True)

    SD_Type = models.CharField(max_length=50, null=True, blank=True)
    SD_Status = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    Network_Type = models.CharField(max_length=50, null=True, blank=True)

    alert_datetime = models.DateTimeField(null=True, blank=True)
    immobilizer = models.BooleanField(default=False)
    IN1 = models.BooleanField(default=False)
    IN2 = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_no or 'Unknown Vehicle'} @ {self.track_time or 'N/A'}"
