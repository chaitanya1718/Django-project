from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Contact

class CustomUserCreationForm(UserCreationForm):
    security_key = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Security Key','autocomplete':'off',}),
        help_text='Enter the registration security key'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','security_key']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_security_key(self):
        key = self.cleaned_data.get('security_key')
        from django.conf import settings
        if key != settings.SECURITY_KEY_FOR_REGISTRATION:
            raise forms.ValidationError("Invalid security key.")
        return key

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'role', 'joining_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'mobile']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}),
        }
