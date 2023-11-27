from django import forms
from django.contrib.auth import authenticate
from .models import UserModel
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password


class SignInForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password', )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'type': 'text',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'type': 'password',
            }),
        }

    def clean(self):
        if not authenticate(**self.cleaned_data):
            raise ValidationError('Incorrect username or password.')


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'type': 'password',
    }))

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'password', )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'type': 'text',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'type': 'text',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'type': 'text',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'type': 'email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'type': 'password',
            }),
        }

    def clean(self):
        username = self.cleaned_data['username']
        try:
            UserModel.objects.get(username=username)
            self.add_error('username', 'User with this username already exist.')
        except UserModel.DoesNotExist:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                self.add_error('confirm_password', 'The confirm password and password are different.')

    def create_user(self):
        del self.cleaned_data['confirm_password']
        UserModel.objects.create_user(**self.cleaned_data)


class EditUserDataForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'type': 'text',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'type': 'text',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'type': 'text',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'type': 'email',
            }),
        }


    def clean_username(self):
        new_username = self.cleaned_data['username']
        user = UserModel.objects.filter(username=new_username).exclude(id=self.instance.pk)
        if user:
            self.add_error('username', 'User with this username already exist.')
        return new_username


class EditPasswordForm(forms.ModelForm):
    new_password = forms.CharField(label='New Password', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password',
        'type': 'password',
    }))
    confirm_password = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'type': 'password',
    }))

    class Meta:
        model = UserModel
        fields = ('password', )
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'type': 'password',
            }),
        }

    def clean(self):
        if not check_password(self.cleaned_data['password'], self.instance.password):
            self.add_error('password', 'Password and actually old password does not match.')

        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'The confirm password and new password are different.')

    def edit_password(self):
        password = self.cleaned_data['new_password']
        self.instance.set_password(password)
        self.instance.save()
