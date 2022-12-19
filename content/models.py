from uuid import uuid4

from django.db import models


class Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, help_text="Category id.")
    title = models.TextField(unique=True, max_length=70,
                             help_text="Category title.")
