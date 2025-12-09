from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('beneficiary', 'Beneficiary'),
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


class Appeal(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('donated', 'Donated'),
        ('authorized', 'Authorized'),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idNumber = models.IntegerField()
    PhoneNumber = models.IntegerField()
    request = models.CharField(max_length=1000)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.user   
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
          return f"{self.user.username} ({self.role}) - {self.email}"
    
