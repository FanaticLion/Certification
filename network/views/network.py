from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from network.models.network import NetworkNode
from network.serializers.network import NetworkNodeSerializer
from network.filters.network import NetworkNodeFilter

class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только активным сотрудникам.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active

class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related(
        'contact', 'supplier'
    ).prefetch_related('products')
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NetworkNodeFilter
    search_fields = ['name', 'contact__country', 'contact__city']
    ordering_fields = ['name', 'created_at', 'debt']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        # Запрещаем обновление поля debt через API
        if 'debt' in serializer.validated_data:
            serializer.validated_data.pop('debt')
        serializer.save()