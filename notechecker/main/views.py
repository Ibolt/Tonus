from django.shortcuts import render
from django.http import HttpResponse
from .models import NoteCheck
from .forms import NoteCheckForm

#Imports for note checking
import aubio
import pyaudio
import numpy as np
import wave
from .noteAnalysis import getNotes
from .noteAnalysis import getChords
from .noteAnalysis import genTabs
from .noteAnalysis import recordToFile

# Create your views here.
#Render HTML Template and pass variables
def home(request):
	return render(request,'main/home.html')

def notes(request):
	#Set default value
	notesList = []
	tabs = []
	
	if request.method == "POST":
		uploaded_file = request.FILES['document']

		#Write data to saved file
		file = open('input.wav', 'wb')
		file.write(uploaded_file.read())

		#Get notes list
		notesList = getNotes('input.wav')
		print(notesList)
		file.close()

		tabs = genTabs(notesList)

	return render(request = request,
		template_name='main/notes.html', 
		context={'notesList': notesList, 'tabs':tabs})

def chords(request):
	#Set default values
	chordsList = []

	if request.method == "POST":

		uploaded_file = request.FILES['document']

		#Write data to saved file
		file = open('input.wav', 'wb')
		file.write(uploaded_file.read())

		#Get notes list
		chordsList = getChords('input.wav')
		print(chordsList)

		#Split list and delete elements so we're left with chord letter and confidence decimal
		chordsList = chordsList[0].split()
		del chordsList[1:3]

		#Make chord letter capital
		chordsList[0] = chordsList[0].upper()

		#Round confidence to a percent
		chordsList[1] = str(round((float(chordsList[1][:-1])*100), 1)) + "%"

		file.close()

	return render(request,'main/chords.html', 
		context={'chordsList': chordsList})

def recording(request):
	name = recordToFile(3)
	chordsList = getChords(name)
	print(chordsList)

	#Split list and delete elements so we're left with chord letter and confidence decimal
	chordsList = chordsList[0].split()
	del chordsList[1:3]

	#Make chord letter capital
	chordsList[0] = chordsList[0].upper()

	#Round confidence to a percent
	chordsList[1] = str(round((float(chordsList[1][:-1])*100), 1)) + "%"


	return render(request, 'main/recording.html',
		context={'chordsList': chordsList})