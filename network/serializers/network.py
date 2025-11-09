from rest_framework import serializers
from network.models.network import Contact, Product, NetworkNode


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'country', 'city', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    hierarchy_level = serializers.ReadOnlyField()

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'contact', 'products',
            'supplier', 'supplier_name', 'debt', 'created_at', 'hierarchy_level'
        ]
        read_only_fields = ['debt', 'created_at', 'hierarchy_level']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        contact = Contact.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact=contact, **validated_data)
        return network_node

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)

        if contact_data:
            contact_serializer = ContactSerializer(
                instance.contact,
                data=contact_data,
                partial=True
            )
            if contact_serializer.is_valid():
                contact_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance