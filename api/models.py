from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('id',)
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, related_name='streets', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Street'
        verbose_name_plural = 'Streets'

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, related_name='shops_city', on_delete=models.CASCADE)
    street = models.ForeignKey(Street, related_name='shops_street', on_delete=models.CASCADE)
    house = models.CharField(max_length=20)
    open = models.TimeField(auto_now=False)
    close = models.TimeField(auto_now=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self):
        return self.name
