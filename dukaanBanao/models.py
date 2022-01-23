from distutils.command.upload import upload
from django.db import models

# Create your models here.

def upload_path(instance, filname):
    return "/".join(["images", filname])

class account(models.Model):
    name = models.CharField(max_length=20)
    phNumber = models.BigIntegerField(unique=True)
    otp = models.IntegerField()
    token = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

class store(models.Model):
    storeName = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    storeURL = models.URLField(max_length=50)
    account_ID = models.ForeignKey(
        account,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return str(self.id)

class image(models.Model):
    img = models.ImageField(upload_to = upload_path, blank=True)

class product(models.Model):
    productName = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    MRP = models.DecimalField(max_digits=8, decimal_places=4)
    image = models.ManyToManyField(image)