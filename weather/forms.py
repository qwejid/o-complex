from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label='Введите город', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Start typing a city name...'}))

    def clean_city(self):
        city = self.cleaned_data['city']
        return city.title()
