from django import forms
from .models import MoviePetition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = MoviePetition
        fields = ["title", "description"]
