from django.db import models
from django.contrib.auth.models import User
from beneficiary.models import Appeal

# Create your models here.
class Donation(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.user.username} donated {self.amount} to {self.appeal.user.username}" 

    