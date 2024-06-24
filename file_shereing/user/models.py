from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class OTPToken(models.Model):
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        # Check if the token is older than 5 minutes
        return timezone.now() - self.created_at <= timezone.timedelta(minutes=5)

    def __str__(self):
        return self.token

class UploadedFile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file.name