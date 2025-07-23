from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from datetime import datetime
from django.utils.timezone import now

class Department(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=25)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    joining_date = models.DateField(default=now,null=True, blank=True)

     
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Contact: {self.email}"



class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.message[:30]}"