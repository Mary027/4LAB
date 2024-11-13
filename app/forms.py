from django import forms
from .models import Event
from django.core.exceptions import ValidationError
import datetime
#создаем форму 
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description', ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
#проверка даты на валидацию
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise ValidationError("Обязательно впишите дату.")
        if date < datetime.date.today():
            raise ValidationError("Дата не может быть в прошлом.")
        return date
