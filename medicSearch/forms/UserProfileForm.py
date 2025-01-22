from django.forms import ModelForm
from django import forms
from medicSearch.models.Profile import Profile

class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'birthday', 'image']
        widgets = {
            'user': forms.HiddenInput(),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }