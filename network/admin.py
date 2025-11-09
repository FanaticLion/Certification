from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from network.models.network import Contact, Product, NetworkNode


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'country', 'city', 'street', 'house_number']
    list_filter = ['country', 'city']
    search_fields = ['email', 'country', 'city']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']
    list_filter = ['release_date']
    search_fields = ['name', 'model']


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'node_type',
        'hierarchy_level_display',
        'supplier_link',
        'debt',
        'created_at'
    ]
    list_filter = ['node_type', 'contact__city', 'created_at']
    search_fields = ['name', 'contact__country', 'contact__city']
    actions = ['clear_debt']

    def hierarchy_level_display(self, obj):
        return obj.hierarchy_level

    hierarchy_level_display.short_description = 'Уровень иерархии'

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:network_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt=0)
        self.message_user(
            request,
            f'Задолженность очищена для {updated_count} объектов.'
        )

    clear_debt.short_description = 'Очистить задолженность перед поставщиком'