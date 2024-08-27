from django.db import models
from django.utils import timezone
from django.conf import settings

STATUS = ((0, "Incomplete"), (1, "Complete"))

class UserProfile(models.Model):
    """
    Model to represent extended auth User Class to add additional
    profile information.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_spoons = models.PositiveIntegerField(blank=True, default=12)

    def __str__(self):
        return f"Profile for {self.user.username}"

    def __str__(self):
        return f"Profile for {self.username}"

class Todo(models.Model):
    title = models.CharField(max_length=100, unique=True)
    details = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated
    spoons_required = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title