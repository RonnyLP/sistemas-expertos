from django import forms

CLASS_CHOICES = [
    ("First", "First"),
    ("Second", "Second"),
    ("Third", "Third"),
]

SEX_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
]

DECK_CHOICES = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
    ("unknown", "Unknown"),
]

TOWN_CHOICES = [
    ("Cherbourg", "Cherbourg"),
    ("Southampton", "Southampton"),
    ("Queenstown", "Queenstown"),
]

ALONE_CHOICES = [
    ("y", "Yes"),
    ("n", "No"),
]


class PredictionForm(forms.Form):

    sex = forms.ChoiceField(
        choices=SEX_CHOICES
    )

    age = forms.FloatField()

    n_siblings_spouses = forms.IntegerField()

    parch = forms.IntegerField()

    fare = forms.FloatField()

    passenger_class = forms.ChoiceField(
        choices=CLASS_CHOICES
    )

    deck = forms.ChoiceField(
        choices=DECK_CHOICES
    )

    embark_town = forms.ChoiceField(
        choices=TOWN_CHOICES
    )

    alone = forms.ChoiceField(
        choices=ALONE_CHOICES
    )
