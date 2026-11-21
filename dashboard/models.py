from django.db import models
from django.utils import timezone

# Create your models here.

class PageView(models.Model):
    """Track page views for analytics"""
    page_name = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']


class UserEvent(models.Model):
    """Track user events like clicks, searches, etc."""
    event_type = models.CharField(max_length=100)
    event_data = models.JSONField(default=dict)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']

class DashboardWidget(models.Model):
    """Configurable dashboard widgets"""
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50)  # chart, stat, list, etc.
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SystemHealth(models.Model):
    """System health monitoring"""
    component = models.CharField(max_length=100)
    status = models.CharField(max_length=20)  # healthy, warning, critical, down
    message = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']

