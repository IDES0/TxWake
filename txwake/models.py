from django.db import models
from django.contrib.auth.models import User

class BoatPull(models.Model):
    date = models.DateField()
    time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=8)
    available_spots = models.PositiveIntegerField(default=8)
    is_active = models.BooleanField(default=False)  # Whether users can sign up

    def __str__(self):
        return f"{self.date} at {self.time} - Spots Left: {self.available_spots}"


class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boat_pull = models.ForeignKey(BoatPull, on_delete=models.CASCADE)
    signup_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'boat_pull']

    def __str__(self):
        return f"{self.user.username} signed up for {self.boat_pull}"