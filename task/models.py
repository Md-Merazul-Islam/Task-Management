from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Task (models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    status= models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=255, blank=True)
    media = models.FileField(upload_to='task_media/', blank=True,null=True)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.created_by and hasattr(self, 'request') and self.request.user.is_authenticated:
            self.created_by = self.request.user
        super().save(*args, **kwargs)
    
    
    def is_images(self):
        if self.media :
            return self.media.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
        return False
    
    def is_videos(self):
        if self.media :
            return self.media.name.lower().endswith(('.mp4', '.avi', '.mov','mkv'))
        return False
    
    def __str__(self):
        return self.title
    

    
    