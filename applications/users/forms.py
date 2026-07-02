from django import forms
from django.core.exceptions import ValidationError
from .models import User


INPUT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'

class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'correo@ejemplo.com'}))
    first_name = forms.CharField(label='Nombres', max_length=50, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    last_name = forms.CharField(label='Apellidos', max_length=50, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    occupation = forms.ChoiceField(label='Ocupación', choices=User.OCCUPATION_CHOICES, widget=forms.Select(attrs={'class': INPUT_CLASS}))
    gender = forms.ChoiceField(label='Género', choices=User.GENDER_CHOICES, widget=forms.Select(attrs={'class': INPUT_CLASS}))
    phone = forms.CharField(label='Celular', max_length=15, required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    date_birth = forms.DateField(label='Fecha de nacimiento', required=False, widget=forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Este correo ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'correo@ejemplo.com'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))


class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    password2 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 == password2:
            raise ValidationError('La nueva contraseña debe ser diferente a la actual.')
        return cleaned_data