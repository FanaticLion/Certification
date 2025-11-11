from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from network.models.network import NetworkNode, Product


def home_view(request):
    products = Product.objects.all()
    network_nodes = NetworkNode.objects.all().select_related('contact', 'supplier')

    factories = [node for node in network_nodes if node.node_type == 'factory']
    retail_chains = [node for node in network_nodes if node.node_type == 'retail']
    entrepreneurs = [node for node in network_nodes if node.node_type == 'entrepreneur']

    context = {
        'products': products,
        'factories': factories,
        'retail_chains': retail_chains,
        'entrepreneurs': entrepreneurs,
        'total_products': products.count(),
        'total_nodes': network_nodes.count(),
    }
    return render(request, 'home.html', context)


def product_catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})


def stores_map(request):
    nodes = NetworkNode.objects.all().select_related('contact')
    return render(request, 'stores.html', {'nodes': nodes})


urlpatterns = [
    path('', home_view, name='home'),
    path('catalog/', product_catalog, name='catalog'),
    path('stores/', stores_map, name='stores'),
    path('admin/', admin.site.urls),
    path('api/', include('network.urls')),
    path('api/auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)