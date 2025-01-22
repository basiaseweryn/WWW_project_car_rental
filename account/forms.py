from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from account.models import Account


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',
                  'address', 'license_number', 'password1', 'password2')

    def clean_email(self): #email validation
        email = self.cleaned_data.get('email')
        if email:
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                #checking if an account with this email exists
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email already registered")
        return email

    def clean_username(self): #username validation
        username = self.cleaned_data.get('username')
        if username:
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                #checking if taken
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username already registered")
        return username

    def clean_phone(self): #phone validation
        phone = self.cleaned_data.get('phone')
        if phone:
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
                #checking if already taken
            except Account.DoesNotExist:
                return phone
            raise forms.ValidationError("Phone already registered")
        return phone

    def clean_license_number(self): #license number validation
        license_number = self.cleaned_data.get('license_number')
        if license_number:
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(license_number=license_number)
            except Account.DoesNotExist:
                return license_number
            raise forms.ValidationError("Licence number already registered")
        return license_number


class AccountAuthentificationForm(forms.ModelForm): #login form
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self): #password validation
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Incorrect Email or Password")
        else:
            raise forms.ValidationError("Enter a correct email")


class AccountUpdateForm(forms.ModelForm): #changing email or username - decided not to use that
    class Meta:
        model = Account
        fields = ( 'email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email already registered")

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username already registered")

