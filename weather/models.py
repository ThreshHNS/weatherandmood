from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    country = models.CharField(max_length=30, help_text="Введите название страны (например: Россия, Канада, Украина)")
    location = models.CharField(max_length=25, blank=True, help_text="Введите координаты города (например: Широта: 59°56′19″ с.ш. Долгота: 30°18′50″ в.д)")

    def __str__(self):
        return self.name

    class Meta:
    	verbose_name_plural = 'cities'

class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='Time')
    temp = models.IntegerField(verbose_name='Temperature')
    night = models.IntegerField(verbose_name='Temperature night')
    wind = models.IntegerField(verbose_name='Wind')
    humidity = models.IntegerField(verbose_name='Cloudiness')
    direction = models.CharField(verbose_name='Direction of wind', max_length=8)
    icon = models.CharField(verbose_name='Icon', max_length=4)

    def __str__(self):
        return "{0} {1}".format( self.city, self.time.strftime('%d-%m-%y') )