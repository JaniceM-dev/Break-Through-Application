from django import forms
from django.forms import ModelForm
from .models import  Appeal , Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomRegistrationForm(UserCreationForm):
    
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data["role"]
            )

        return user


class  AppealForm(ModelForm):
    class Meta:
        model =  Appeal
        fields = '__all__'
        exclude = ['user']


class MessageForm(ModelForm):
    class Meta:
        model =  Message
        fields = '__all__'
        exclude =  exclude = ['user', 'role', 'created_at', 'updated_at']