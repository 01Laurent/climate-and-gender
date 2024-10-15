from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from  .models import UserProfile


class UserForm(UserCreationForm):
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age'
                }
            )
    )
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your location'
                }
            )
    )
    health_condition = forms.ChoiceField(
        choices=UserProfile.HEALTH_CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
                }
            )
    )
    next_of_kin = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin phone number'
                }
            )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                location=self.cleaned_data['location'],
                health_condition=self.cleaned_data['health_condition'],
                phone=self.cleaned_data['phone'],
                next_of_kin=self.cleaned_data['next_of_kin']
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
                "age",
                "gender",
                "location",
                "health_condition",
                "email",
                "phone",
                "next_of_kin"
                ]
        labels = {
                "age": "Age",
                "gender": "Gender",
                "location": "Location",
                "health_condition": "Health Condition",
                "email": "Email",
                "phone": "Phone",
                "next_of_kin": "Next of Kin"
                }
