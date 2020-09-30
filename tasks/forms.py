from django import forms
from .models import Task
from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.validators import ValidationError


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ReadingsForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'completion_date', 'status')
