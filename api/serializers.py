from rest_framework.serializers import ModelSerializer, CharField

from .models import City, Street, Shop


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class StreetSerializer(ModelSerializer):
    class Meta:
        model = Street
        exclude = ['city']


class ShopSerializer(ModelSerializer):
    city = CharField()
    street = CharField()

    class Meta:
        model = Shop
        exclude = ['id']

    def create(self, validated_data):
        city = City.objects.filter(name=validated_data['city']).first()
        if not city:
            validated_data['city'] = City.objects.create(name=validated_data['city'])

        street = Street.objects.filter(name=validated_data['street'], city=validated_data['city']).first()
        if not street:
            validated_data['street'] = Street.objects.create(name=validated_data['street'], city=validated_data['city'])

        return Shop.objects.create(**validated_data)
