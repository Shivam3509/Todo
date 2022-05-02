from django.urls import path
from .views import Index
urlpatterns = [
    path('index/', Index, name='index'),
]