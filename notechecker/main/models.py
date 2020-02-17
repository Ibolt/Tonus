from django.db import models
from .forms import NoteCheckForm
# Create your models here.

class NoteCheck(models.Model):
	audio_file = models.FileField(upload_to='uploads/')