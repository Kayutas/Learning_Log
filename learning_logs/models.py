from django.db import models

# Create your models here.


class Topic(models.Model):
    """A Topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    def _str_(self):
        """Return a string representation of the model."""
        return self.text
