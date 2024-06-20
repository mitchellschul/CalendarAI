from django import forms
from .models import Task

HOUR_CHOICES = [(str(i), f"{i:02d}") for i in range(1, 13)]
MINUTE_CHOICES = [(str(i), f"{i:02d}") for i in range(0, 60, 15)]  # Using 15-minute intervals
PERIOD_CHOICES = [('AM', 'AM'), ('PM', 'PM')]

class TaskForm(forms.ModelForm):
    start_hour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, required=False)
    start_period = forms.ChoiceField(choices=PERIOD_CHOICES, required=False)
    end_hour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, required=False)
    end_period = forms.ChoiceField(choices=PERIOD_CHOICES, required=False)
    no_specific_time = forms.BooleanField(label='No Specific Time', required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('no_specific_time'):
            cleaned_data['start_hour'] = None
            cleaned_data['start_minute'] = None
            cleaned_data['start_period'] = None
            cleaned_data['end_hour'] = None
            cleaned_data['end_minute'] = None
            cleaned_data['end_period'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('no_specific_time'):
            instance.start_time = None
            instance.end_time = None
        else:
            start_hour = self.cleaned_data.get('start_hour')
            start_minute = self.cleaned_data.get('start_minute')
            start_period = self.cleaned_data.get('start_period')
            end_hour = self.cleaned_data.get('end_hour')
            end_minute = self.cleaned_data.get('end_minute')
            end_period = self.cleaned_data.get('end_period')

            if start_hour and start_minute and start_period:
                start_hour = int(start_hour)
                start_minute = int(start_minute)
                if start_period == 'PM' and start_hour != 12:
                    start_hour += 12
                if start_period == 'AM' and start_hour == 12:
                    start_hour = 0
                instance.start_time = f"{start_hour:02d}:{start_minute:02d}:00"
            else:
                instance.start_time = None

            if end_hour and end_minute and end_period:
                end_hour = int(end_hour)
                end_minute = int(end_minute)
                if end_period == 'PM' and end_hour != 12:
                    end_hour += 12
                if end_period == 'AM' and end_hour == 12:
                    end_hour = 0
                instance.end_time = f"{end_hour:02d}:{end_minute:02d}:00"
            else:
                instance.end_time = None

        if commit:
            instance.save()

        return instance
