from django.db import models


class Story(models.Model):
    tag = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.tag  # This controls how the model instance is displayed
