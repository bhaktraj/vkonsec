from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT'),
    )
   
    user_type = models.CharField(choices=USER,max_length=50,default=1)
    userid = models.IntegerField(primary_key=True, unique=True, default=10001)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    email =models.EmailField()
    phone = models.TextField()
    course = models.TextField()
    msg = models.TextField()
    date = models.DateField(auto_now_add=True)
# Create your models here.
