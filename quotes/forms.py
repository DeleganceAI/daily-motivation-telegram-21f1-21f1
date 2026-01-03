from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User, UserPreference, Category


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user preferences
            UserPreference.objects.create(user=user)
        return user


class UserPreferenceForm(forms.ModelForm):
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        help_text='Select your preferred time to receive quotes (UTC)'
    )

    class Meta:
        model = UserPreference
        fields = ['preferred_categories', 'delivery_paused']
        widgets = {
            'preferred_categories': forms.CheckboxSelectMultiple(),
            'delivery_paused': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.initial['preferred_time'] = self.instance.user.preferred_time

    def save(self, commit=True):
        preference = super().save(commit=False)
        if 'preferred_time' in self.cleaned_data:
            preference.user.preferred_time = self.cleaned_data['preferred_time']
            if commit:
                preference.user.save()
        if commit:
            preference.save()
            self.save_m2m()
        return preference


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
