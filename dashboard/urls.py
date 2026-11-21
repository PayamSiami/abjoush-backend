from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('api/analytics-overview/', views.api_analytics_overview, name='api_analytics_overview'),
    path('api/page-stats/', views.api_page_stats, name='api_page_stats'),
    path('api/event-types/', views.api_event_types, name='api_event_types'),
    path('api/widgets/', views.api_widgets, name='api_widgets'),
    path('api/system-health/', views.api_system_health, name='api_system_health'),
    path('api/health-check/', views.api_health_check, name='api_health_check'),
]
