from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, blank=True, null=True)
    filepath = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.filename if self.filename else self.filepath.name

