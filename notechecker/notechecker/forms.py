from django import forms

class NoteCheckForm(forms.Form):
	audio = forms.FileField(upload_to='uploads/',
		allow_empty_file=True)