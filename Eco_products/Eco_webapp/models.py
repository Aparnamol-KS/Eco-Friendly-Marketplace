from django.db import models

# Create your models here.

from django.db import models

class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Password can be stored as hashed
    role = models.CharField(
        max_length=10, 
        choices=(('Buyer', 'Buyer'), ('Admin', 'Admin'))
    )

    def __str__(self):
        return f"{self.name} ({self.email})"

