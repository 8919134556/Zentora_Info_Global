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






class CurrentTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    clientid = models.CharField(max_length=150, blank=True, null=True)
    vehicleno = models.CharField(max_length=150, blank=True, null=True)
    unitno = models.CharField(max_length=50)
    
    ignition = models.SmallIntegerField()  # 0 or 1
    tracktime = models.DateTimeField()
    
    speed = models.FloatField(blank=True, null=True)
    gpsstatus = models.SmallIntegerField(blank=True, null=True)  # 0 or 1
    direction = models.CharField(max_length=20)
    
    lat = models.FloatField()
    lon = models.FloatField()
    
    odometer = models.BigIntegerField(blank=True, null=True)
    gpsodometer = models.BigIntegerField(blank=True, null=True)
    
    location = models.TextField(blank=True, null=True)
    
    mainpower = models.FloatField(blank=True, null=True)
    devbatterylevel = models.FloatField(blank=True, null=True)
    
    panic = models.SmallIntegerField(blank=True, null=True)  # 0 or 1
    immobalizer = models.SmallIntegerField(blank=True, null=True)  # 0 or 1
    siren = models.SmallIntegerField(blank=True, null=True)  # 0 or 1
    
    overspeed = models.FloatField(blank=True, null=True)
    
    ha = models.CharField(max_length=20, blank=True, null=True)
    hb = models.CharField(max_length=20, blank=True, null=True)
    accident = models.CharField(max_length=20, blank=True, null=True)
    
    temperature = models.FloatField(blank=True, null=True)
    fuellevel = models.FloatField(blank=True, null=True)
    fuellevelltrs = models.FloatField(blank=True, null=True)
    
    x_axis = models.FloatField(blank=True, null=True)
    y_axis = models.FloatField(blank=True, null=True)
    z_axis = models.FloatField(blank=True, null=True)
    
    alerttype = models.CharField(max_length=150, blank=True, null=True)
    
    driverid = models.CharField(max_length=150, blank=True, null=True)
    driverrfid = models.CharField(max_length=150, blank=True, null=True)
    drivername = models.CharField(max_length=200, blank=True, null=True)
    
    alertdatetime = models.DateTimeField()
    
    devicetype = models.CharField(max_length=150, blank=True, null=True)
    
    createddate = models.DateTimeField(auto_now_add=True)
    
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'current_table'
        managed = False  # Django will NOT try to create or modify the table

    def __str__(self):
        return f"{self.unitno} - {self.vehicleno}"