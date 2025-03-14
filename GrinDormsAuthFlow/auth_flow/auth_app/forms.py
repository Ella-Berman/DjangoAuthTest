from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.core.exceptions import ValidationError

# Create/register a user (Model Form)
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:

        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        
        if not email.endswith('@grinnell.edu'):
            raise ValidationError("Please use your Grinnell College email address.")
        return email
        

# Authenticate a user (Model Form)
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# class ResetPasswordForm(PasswordResetForm):
#     email = forms.EmailField(label="Email Address")
