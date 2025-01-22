from datetime import datetime

from django import forms

from rental.models import RentalRecord, City


class SearchForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        empty_label="Select a city"
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date",
        required=True,


    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date",
        required=True,
    )

    class Meta:
        model = RentalRecord
        fields = ['start_date', 'end_date', 'city']

    def clean(self):
        if self.is_valid():
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')

            if start_date and end_date and start_date > end_date:
                raise forms.ValidationError("Start date must be before end date.")
            if start_date.strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
                raise forms.ValidationError("Start date must be in the future.")
        else:
            raise forms.ValidationError("Please enter a valid date range.")

""""    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Incorrect Email or Password")
        else:
            raise forms.ValidationError("Enter a correct email")"""
from django import forms


class BookingForm(forms.Form):
    is_driver_under_25 = forms.BooleanField(
        required=False,
        label="Is the driver younger than 25 years old?"
    )

    is_not_driver = forms.BooleanField(
        required=False,
        label="Are you NOT the driver?"
    )

    driver_name = forms.CharField(
        max_length=100,
        required=False,
        label="Driver's First Name"
    )

    driver_surname = forms.CharField(
        max_length=100,
        required=False,
        label="Driver's Last Name"
    )

    driver_license_number = forms.CharField(
        max_length=50,
        required=False,
        label="Driver's License Number"
    )

    add_insurance = forms.BooleanField(
        required=False,
        label="Do you want to insure the car? (+20% of base price)"
    )

    def clean(self):
        cleaned_data = super().clean()
        is_not_driver = cleaned_data.get('is_not_driver')

        if is_not_driver:
            if not cleaned_data.get('driver_name'):
                self.add_error('driver_name', 'Driver\'s first name is required.')
            if not cleaned_data.get('driver_surname'):
                self.add_error('driver_surname', 'Driver\'s last name is required.')
            if not cleaned_data.get('driver_license_number'):
                self.add_error('driver_license_number', 'Driver\'s license number is required.')

