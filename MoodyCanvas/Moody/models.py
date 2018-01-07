from django.db import models

# Create your models here.
class Customer(models.Model):
    cust_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cust_name

class Plate(models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plate_id = models.CharField(max_length=50)
    plate_sn = models.CharField(max_length=50)
    plate_mfr = models.CharField(max_length=50)
    plate_wid = models.IntegerField()
    plate_len = models.IntegerField()
    
    def __str__(self):
        return self.plate_id

class Verif(models.Model):
    plate_id = models.ForeignKey(Plate, on_delete=models.CASCADE)
    verif_date = models.DateTimeField('date performed')
    verif_foot = models.IntegerField()
    verif_north = models.IntegerField(default=4)
    verif_NS = models.IntegerField()
    verif_EW = models.IntegerField()
    verif_top = models.FloatField()
    verif_bot = models.FloatField()
    verif_start = models.FloatField()
    verif_end = models.FloatField()
    verif_rep = models.IntegerField()
    verif_flat = models.IntegerField()
    verif_grade = models.CharField(max_length=4)
    verif_len = models.IntegerField()
    verif_wid = models.IntegerField()
    verif_diag = models.IntegerField()
    clos_7 = models.IntegerField()
    clos_8 = models.IntegerField()
    verif_cert = models.TextField(max_length=50)
    verif_tech = models.TextField(max_length=50)
    verif_descr = models.TextField(max_length=50)
    verif_min = models.IntegerField()
    verif_max = models.IntegerField()

    def __str__(self):
        return str(self.verif_date.date())

class Profile(models.Model):
    verif_id = models.ForeignKey(Verif, on_delete=models.CASCADE)
    profile_id = models.IntegerField()

    def __str__(self):
        return str(self.profile_id)

class Meas(models.Model):
    verif_id = models.ForeignKey(Verif, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    measurement = models.FloatField()

    def __str__(self):
        return str(self.id) + ': ' + str(self.measurement)
    

