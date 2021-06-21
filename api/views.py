from datetime import datetime

from django.db.models import Q, F
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
            time = datetime.now().time()
            q = Q()

            if street_name is not None:
                q.add(Q(street__name=street_name), Q.AND)

            if city_name is not None:
                q.add(Q(city__name=city_name), Q.AND)

            if open is not None:
                if open == "1":
                    q.add(Q(
                        Q(open__lt=F('close')), Q(open__lte=time), Q(close__gt=time)) |
                          Q(Q(open__gt=F('close')), Q(Q(open__lte=time) | Q(close__gt=time))) | Q(open=F('close')),
                          Q.AND)
                elif open == "0":
                    q.add(Q(
                        Q(open__lt=F('close')), Q(Q(open__gt=time) | Q(close__lte=time))) |
                          Q(Q(open__gt=F('close')), Q(open__gt=time), Q(close__lte=time)), Q.AND)
                else:
                    raise ValueError

            queryset = Shop.objects.filter(q)
            serialized = ShopSerializer(queryset, many=True)

            return Response(serialized.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
