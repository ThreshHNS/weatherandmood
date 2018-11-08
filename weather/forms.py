from django import forms
from .models import City
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import requests

class CityForm(forms.Form):

	name = forms.CharField(label='add_city', widget=forms.TextInput(attrs={'type' : 'text', 'placeholder' : 'Add your location...'}))
	
	def clean_name(self):

		name = self.cleaned_data['name']

		# If city is string with digits - > raise ValidationError
		if name.isdigit():
			raise ValidationError(_('The city name cannot be a number.'))

		# If city already exists in our db - > raise ValidationError
		if City.objects.filter(name=name).exists():
			print('Name of city exists')
			raise ValidationError(_('The city name already exists.'))

		# If OpenWeatherMap API have not found city -> rase ValidationError
		url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=af6b64750bf392c94ec8ff16e6b2d41a'

		r = requests.get(url.format(name)).json()

		if r['cod'] == '404':	
			raise ValidationError(_('The name of the city not found.'))

		return name
