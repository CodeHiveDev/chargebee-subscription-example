from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# This table is used for signup, login, and authentication process.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.DateTimeField(default=timezone.now)
    modified_by = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100, default="normal")
    status = models.CharField(max_length=100, default="Active")
    auth_provider = models.CharField(
        max_length=50, blank=True, default='email')


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.CharField(max_length=500)
    amount = models.CharField(max_length=400)
    item_price_id = models.CharField(max_length=400)
    customer_id = models.CharField(max_length=400)
    status = models.CharField(max_length=400)
    start_date =  models.DateField()

