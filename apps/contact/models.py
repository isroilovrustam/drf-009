from django.db import models
from shared.models import BaseModel


class Contact(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    message = models.TextField()

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
