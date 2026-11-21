from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.db.models import Count

from .models import PageView, UserEvent, DashboardWidget, SystemHealth

# Create your views here.

def dashboard_home(request):
    """Render the main dashboard page"""
    return render(request, 'dashboard/home.html')

@csrf_protect
def api_analytics_overview(request):
    """API endpoint for dashboard analytics overview"""
    if request.method == 'GET':
        # Get recent page views (last 24 hours)
        recent_views = PageView.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        # Get recent events (last 24 hours)
        recent_events = UserEvent.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        # Get active widgets
        active_widgets = DashboardWidget.objects.filter(is_active=True).count()
        
        # Get system health status
        recent_health = SystemHealth.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).order_by('-timestamp').first()
        
        health_status = 'healthy'
        if recent_health:
            health_status = recent_health.status
        
        data = {
            'recent_views': recent_views,
            'recent_events': recent_events,
            'active_widgets': active_widgets,
            'system_health': health_status,
            'last_updated': timezone.now().isoformat(),
        }
        
        return JsonResponse(data)

@csrf_protect
def api_page_stats(request):
    """API endpoint for page statistics"""
    if request.method == 'GET':
        # Get page views grouped by page name for last 7 days
        page_stats = PageView.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).values('page_name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Convert to list format
        stats_list = [
            {'page': stat['page_name'], 'views': stat['count']}
            for stat in page_stats
        ]
        
        return JsonResponse({'page_stats': stats_list})

@csrf_protect
def api_event_types(request):
    """API endpoint for event type statistics"""
    if request.method == 'GET':
        event_stats = UserEvent.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).values('event_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        stats_list = [
            {'event_type': stat['event_type'], 'count': stat['count']}
            for stat in event_stats
        ]
        
        return JsonResponse({'events': stats_list})

@csrf_protect
def api_widgets(request):
    """API endpoint for dashboard widgets"""
    if request.method == 'GET':
        widgets = DashboardWidget.objects.filter(is_active=True)
        widgets_list = [
            {
                'id': widget.id,
                'name': widget.name,
                'widget_type': widget.widget_type,
                'config': widget.config
            }
            for widget in widgets
        ]
        return JsonResponse({'widgets': widgets_list})

@csrf_protect
def api_system_health(request):
    """API endpoint for system health status"""
    if request.method == 'GET':
        health_records = SystemHealth.objects.filter(
            timestamp__gte=timezone.now() - timedelta(hours=24)
        ).order_by('timestamp')
        
        health_list = [
            {
                'timestamp': record.timestamp.isoformat(),
                'component': record.component,
                'status': record.status,
                'message': record.message
            }
            for record in health_records
        ]
        
        return JsonResponse({'health_records': health_list})

@csrf_protect
def api_health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'django-dashboard-api'
    })

