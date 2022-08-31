from django import forms
from .models import Review

class AsideForm(forms.Form):
    search = forms.CharField(label="",max_length=100)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
