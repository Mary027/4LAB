# Импорт модуля models из библиотеки Django
from django.db import models
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.name