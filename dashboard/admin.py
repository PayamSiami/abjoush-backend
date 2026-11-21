from django.contrib import admin
from .models import PageView, UserEvent, DashboardWidget, SystemHealth

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'timestamp', 'ip_address']
    list_filter = ['timestamp', 'page_name']
    search_fields = ['page_name', 'ip_address']
    date_hierarchy = 'timestamp'

@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['event_type', 'user__username']
    date_hierarchy = 'timestamp'

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'is_active', 'updated_at']
    list_filter = ['widget_type', 'is_active']
    search_fields = ['name']

@admin.register(SystemHealth)
class SystemHealthAdmin(admin.ModelAdmin):
    list_display = ['component', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['component', 'message']
    date_hierarchy = 'timestamp'
