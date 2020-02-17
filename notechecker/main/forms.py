from django import forms

class NoteCheckForm(forms.Form):
	audio = forms.FileField()