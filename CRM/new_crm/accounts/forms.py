from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text='Enter your full name.')
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']  # Store full name in first_name for demo
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user