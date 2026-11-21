#!/usr/bin/env python
"""
Seed data script for testing the dashboard
"""
import os
import django
import random
from datetime import timedelta

from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from dashboard.models import PageView, UserEvent, DashboardWidget, SystemHealth
from django.contrib.auth.models import User

def seed_data():
    print("Seeding dashboard data...")
    now = timezone.now()
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'is_active': True}
    )
    
    # Create sample page views
    page_names = ['home', 'products', 'about', 'contact', 'dashboard', 'profile', 'settings']
    user_agents = ['Mozilla/5.0', 'Chrome/91.0', 'Safari/605.1', 'Firefox/89.0']
    
    PageView.objects.all().delete()
    print(f"Creating {100} page views...")
    for i in range(100):
        PageView.objects.create(
            page_name=random.choice(page_names),
            user_agent=random.choice(user_agents),
            ip_address='127.0.0.1' if i % 2 == 0 else f'192.168.1.{i % 255}',
            timestamp=now - timedelta(minutes=random.randint(0, 60))
        )
    
    # Create sample user events
    event_types = ['click', 'scroll', 'search', 'purchase', 'login', 'logout', 'view_page']
    event_data = {
        'click': {'element': 'button', 'location': 'header'},
        'scroll': {'depth': random.randint(0, 100)},
        'search': {'query': 'coffee', 'results': random.randint(0, 10)},
        'purchase': {'item': 'mug', 'price': 10.99},
        'login': {'method': 'password'},
        'logout': {'session_duration': 3600},
        'view_page': {'duration': 30}
    }
    
    UserEvent.objects.all().delete()
    print(f"Creating {50} user events...")
    for i in range(50):
        event = random.choice(event_types)
        UserEvent.objects.create(
            event_type=event,
            event_data=event_data[event],
            user=user if random.random() < 0.7 else None,
            timestamp=now - timedelta(minutes=random.randint(0, 60))
        )
    
    # Create dashboard widgets
    widgets = [
        {
            'name': 'Recent Activity',
            'widget_type': 'activity_list',
            'config': {'items_per_page': 10}
        },
        {
            'name': 'User Statistics',
            'widget_type': 'stats_chart',
            'config': {'chart_type': 'line', 'time_range': '7d'}
        },
        {
            'name': 'Traffic Sources',
            'widget_type': 'pie_chart',
            'config': {'show_labels': True}
        }
    ]
    
    DashboardWidget.objects.all().delete()
    print(f"Creating {len(widgets)} dashboard widgets...")
    for widget in widgets:
        DashboardWidget.objects.create(**widget)
    
    # Create system health records
    SystemHealth.objects.all().delete()
    components = ['database', 'cache', 'api', 'storage', 'email']
    # status/message pairs kept consistent so the dashboard never shows an
    # "healthy" component that is simultaneously complaining.
    health_samples = [
        ('healthy', ''),
        ('healthy', ''),
        ('healthy', ''),
        ('healthy', 'All checks passed'),
        ('warning', 'High load detected'),
        ('warning', 'Slow response time'),
        ('critical', 'Connection pool exhausted'),
        ('critical', 'Storage nearly full'),
    ]

    print(f"Creating {20} system health records...")
    for i in range(20):
        status, message = random.choice(health_samples)
        SystemHealth.objects.create(
            component=random.choice(components),
            status=status,
            message=message,
            timestamp=now - timedelta(minutes=random.randint(0, 60))
        )
    
    print("Data seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
