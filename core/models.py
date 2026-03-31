from django.db import models
from django.contrib.auth.models import User


# 🔹 Farmer Entry
class FarmerEntry(models.Model):
    farmer_name = models.CharField(max_length=200)
    village = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    acres = models.FloatField()
    crop_type = models.CharField(max_length=100)
    total_bags = models.CharField(max_length=50)
    total_amount = models.FloatField(default=0)
    lorry_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='farmers/', blank=True, null=True)

    def __str__(self):
        return self.farmer_name


# 🔹 Mill Entry
class MillEntry(models.Model):
    owner_name = models.CharField(max_length=200)
    mill_name = models.CharField(max_length=200)
    mill_address = models.CharField(max_length=300)
    district = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    paddy_type = models.CharField(max_length=200)
    bags = models.CharField(max_length=100)
    lorry = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='mills/', blank=True, null=True)

    def __str__(self):
        return self.mill_name


# 🔹 Crop Data
class CropData(models.Model):
    crop_name = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.crop_name


# 🔹 Business Records
class BusinessRecord(models.Model):
    date = models.DateField()
    total_bags = models.IntegerField()
    total_amount = models.FloatField()

    def __str__(self):
        return str(self.date)


# 🔹 Notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


# 🔹 Activity
class Activity(models.Model):
    ENTRY_TYPES = [
        ('Farmer', 'Farmer'),
        ('Mill', 'Mill')
    ]

    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    crop = models.CharField(max_length=50)
    bags = models.IntegerField()
    amount = models.FloatField()
    lorry = models.CharField(max_length=20)
    image = models.ImageField(upload_to='paddy_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.crop


# 🔹 Reports
class Report(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_user")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_by")
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reported_user} reported by {self.reported_by}"


# 🔹 Harvest Farmer (Single Entry Page)
class HarvestFarmer(models.Model):
    farmer_name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    operator_name = models.CharField(max_length=100, default="NA")
    machine_number = models.CharField(max_length=10, default="NA")
    acres = models.FloatField()
    time = models.CharField(max_length=20)
    amount = models.IntegerField()
    bill = models.ImageField(upload_to='bills/')

    def __str__(self):
        return self.farmer_name


class HarvesterOperator(models.Model):
    operator_name = models.CharField(max_length=100)
    machine_number = models.CharField(max_length=20)
    date = models.DateField()

    # farmer details (single row)
    farmer_name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    acres = models.FloatField()
    total_time = models.CharField(max_length=50)
    total_amount = models.FloatField()

    bill = models.ImageField(upload_to='harvester_bills/', blank=True, null=True)

    def __str__(self):
        return self.operator_name
    






    from django.db import models

# Took from mill
class MillTransaction(models.Model):
    date = models.DateField()
    mill_name = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.mill_name


# Given to farmer
class FarmerTransaction(models.Model):
    date = models.DateField()
    farmer_name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.farmer_name