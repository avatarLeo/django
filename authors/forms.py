from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name,'')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at  least one uppercase letter,'
                              'one lowercase letter and one number. The length should be'
                              'at least 8 characters'
                              ),
                              code='invalid'
                              )

        
class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your E-mail')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')


    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs={
                'placeholder': 'Your password'
            }
        ),
        error_messages={
            'required': 'Password must not be empty'
        },

        validators=[strong_password]
    )


    password2 = forms.CharField(
        widget= forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password'
            }
        )
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password'
        }

        help_texts = {
            'email': 'The e-mail must be valid'
        }

        widgets = {
            'first_name':forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            }),
            'password':forms.PasswordInput(attrs={
                'placeholder': 'Type password here'
            }),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'carro' in data:
            raise ValidationError('there one error on password')

        return data

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if not password == password2:
            raise ValidationError({
                "password":"Password it's not equals",
                "password2":"Password it's not equals"
                }
            )
