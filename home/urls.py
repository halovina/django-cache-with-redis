from django.urls import path
from .views import redis_manage_data

urlpatterns = [
    path('manage-data', redis_manage_data, name="manage-data-redis"),
]