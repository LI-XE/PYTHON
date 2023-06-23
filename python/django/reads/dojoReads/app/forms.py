from django import forms
from django.forms.widgets import TextInput
from .models import *


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
