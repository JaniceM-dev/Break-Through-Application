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
        fields = ["username", "password1", "password2", "role" , 'email']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data["role"]
            )

        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class  AppealForm(ModelForm):
    class Meta:
        model =  Appeal
        fields = [
             'idNumber',
            'PhoneNumber',
            'request'
        ]

        widgets = {
            'idNumber': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your ID number',
                'required': True
            }),
            'PhoneNumber': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': True
            }),
            'request': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe your request in detail...',
                'required': True
            }),
        }

        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['idNumber'].required = True
            self.fields['PhoneNumber'].required = True
            self.fields['request'].required = True


class MessageForm(ModelForm):
    class Meta:
        model =  Message
        fields = '__all__'
        exclude = ['user', 'role', 'created_at', 'updated_at']

        widgets = {
                    'email': forms.EmailInput(attrs={
                        'class': 'form-control rounded-pill',
                        'placeholder': 'Enter your email',
                        'required': True
                    }),
                    'message': forms.Textarea(attrs={
                        'class': 'form-control rounded-3',
                        'placeholder': 'Type your message here...',
                        'rows': 5,
                        'required': True
                    }),
                }        
  