from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from account.models import Account


class City(models.Model):
    city = models.CharField(max_length=50, unique =True)
    country = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.city}, {self.country}"

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    year = models.IntegerField()
    dailyPrice = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year} {self.dailyPrice}"

class RentalRecord(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if (self.end_date - self.start_date) > timedelta(days=21):
                raise ValidationError("Rental period cannot be more than 3 weeks.")
        else:
            raise ValidationError("Both start date and end date are required.")

