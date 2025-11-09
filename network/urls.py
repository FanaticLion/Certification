from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.network import NetworkNodeViewSet

router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet, basename='network-node')

urlpatterns = [
    path('', include(router.urls)),
]