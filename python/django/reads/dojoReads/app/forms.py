from django import forms
from django.forms.widgets import TextInput
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    # def save(self, commit=True):
    #     # cleaned_data = super(RegisterForm, self).clean()
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user

    # def clean(self):
    #     cleaned_data = super(RegisterForm, self).clean()

    #     if len(cleaned_data["username"]) < 3:
    #         self.add_error(
    #             "username", "Username must be at least 3 characters.")

        # email_check = User.objects.filter(email=cleaned_data['email'])
        # if len(email_check) > 0:
        #     self.add_error("email", "Email already in use")

        # if len(cleaned_data["password"]) < 8:
        #     self.add_error(
        #         "password", "Password must be at least 8 characters")

        # if cleaned_data["password"] != cleaned_data["confirm"]:
        #     self.add_error("password", "Password DO not match.")


class LogForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=50, min_length=2)
#     alios = forms.CharField(max_length=255, min_length=2)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=100, widget=forms.PasswordInput)
#     confirm_password = forms.CharField(
#         max_length=100, widget=forms.PasswordInput)


# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
    # fields = "__all__"

    # def clean(self):
    #     cleaned_data = super(User, self).clean()

    #     if len(cleaned_data["username"]) < 3:
    #         self.add_error(
    #             "username", "Username must be at least 3 characters.")

    #     if len(cleaned_data["alios"]) < 3:
    #         self.add_error("alios", "Alios must be at least 3 characters.")

    #     email_check = User.objects.filter(email=cleaned_data['email'])
    #     if len(email_check) > 0:
    #         self.add_error("email", "Email already in use")

    #     if len(cleaned_data["password"]) < 8:
    #         self.add_error(
    #             "password", "Password must be at least 8 characters")

    #     if cleaned_data["password"] != cleaned_data["confirm"]:
    #         self.add_error("password", "Password DO not match.")


class ReviewForm(forms.Form):
    review = forms.CharField(max_length=255, min_length=2,
                             label="Book Review:"
                             #  , widget=TextInput(attrs={})
                             )
    rating = forms.IntegerField(label="Book Rating:", min_value=0, max_value=5)


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("review", "rating")     # "__all__"
        labels = {
            "review": "Book Review",
            "rating": "Book Rating"
        }
