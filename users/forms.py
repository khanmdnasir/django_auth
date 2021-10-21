from django import forms
from django.contrib.auth import password_validation
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext,gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class RegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone_number=PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BD',attrs={'class':'form-control'}))
    
    class Meta:
        model=User
        fields=['username','email','password1','password2','phone_number','is_teacher']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}


class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label=_("Confirm Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email=forms.CharField(label=_('Email'),widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )



class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')