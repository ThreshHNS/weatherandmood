from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)
    country = models.CharField(max_length=30, help_text="Введите название страны (например: Россия, Канада, Украина)")
    location = models.CharField(max_length=25, blank=True, help_text="Введите координаты города (например: Широта: 59°56′19″ с.ш. Долгота: 30°18′50″ в.д)")

    def __str__(self):
        return self.name

    class Meta:
    	verbose_name_plural = 'cities'