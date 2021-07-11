from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Tasks_List


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)




class TaskForm(forms.ModelForm):

    class Meta:
        model = Tasks_List
        fields = {'task','complete'}

