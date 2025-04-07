from django import forms
from .models import UserProfile
from django.contrib.auth.models import User



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'address', 'mobile', 'gender']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class RegisterForm(forms.ModelForm):
    u_password = forms.CharField(widget=forms.PasswordInput)
    u_age = forms.IntegerField()
    u_address = forms.CharField()
    u_mobile = forms.CharField()
    u_gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "u_password"]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["u_password"],
        )
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                age=self.cleaned_data["u_age"],
                address=self.cleaned_data["u_address"],
                mobile=self.cleaned_data["u_mobile"],
                gender=self.cleaned_data["u_gender"],
            )
            profile.save()
        return user


class LoginForm(forms.Form):
    u_name = forms.CharField(max_length=150)
    u_password = forms.CharField(widget=forms.PasswordInput)