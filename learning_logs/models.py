from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    """Category for organizing topics."""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name


class Topic(models.Model):
    """A Topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        """Return a string representation of the model."""
        return self.text
    
    
    


class Entry(models.Model):
    """Someting specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'entries'
        
    def __str__(self):
        """Return a simple string representation of the entry."""
        return f"{self.text[:50]}..."
    # The [:50] slice limits the string to the first 50 characters.


class Following(models.Model):
    """Represents a following relationship between users."""
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class Comment(models.Model):
    """Comments on topics."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return f"{self.author.username}'s comment on {self.topic.text}"
