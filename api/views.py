from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import City, Street, Shop
from .serializers import CitySerializer, StreetSerializer, ShopSerializer


class CitiesListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class CityStreetsListView(ListAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        try:
            city_id = self.request.query_params.get('city_id')
            queryset = Street.objects.filter(city_id=city_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShopSet(ViewSet):

    def create(self, request):
        try:
            serializer = ShopSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            shop = serializer.save()
            return Response({'shop_id': shop.id})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            street_name = self.request.query_params.get('street')
            city_name = self.request.query_params.get('city')
            open = self.request.query_params.get('open')

            q = Q()
            if street_name is not None:
                q.add(Q(street__name=street_name), Q.AND)

            if city_name is not None:
                q.add(Q(city__name=city_name), Q.AND)

            queryset = Shop.objects.filter(q)
            serialized = ShopSerializer(queryset, many=True)

            if open is not None:
                if (open == '1' or open == '0'):
                    open = int(open)
                    data = [item for item in serialized.data if item['opened'] == open]
                    return Response(data)
                else:
                    raise ValueError

            return Response(serialized.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
