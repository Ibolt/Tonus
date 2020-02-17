import aubio
import pyaudio
import numpy as np
import wave
from subprocess import Popen, PIPE
import aubio
from aubio import source, onset, notes
import PIL
#from PIL import image
import math

#Record audio and save to wav file
def recordToFile(seconds):
	format = pyaudio.paInt16
	channels = 2
	rate = 44100
	chunk = 1024
	time = seconds

	p = pyaudio.PyAudio()

	stream = p.open(format=format, channels=channels, rate=rate,
		input=True, frames_per_buffer=chunk)

	frames = []

	print("Starting recording")

	#Read data from stream and append it to a list
	for i in range(0, int(rate / chunk * time)):
		data = stream.read(chunk)
		frames.append(data)

	print("Finished recording")

	#Stop recording
	stream.stop_stream()
	stream.close()
	p.terminate()

	#Write data to file
	filename = "recordedAudio.wav"
	file = wave.open(filename, 'wb')
	file.setnchannels(channels)
	file.setsampwidth(p.get_sample_size(format))
	file.setframerate(rate)
	#Join frames list into string
	file.writeframes(b''.join(frames))
	file.close()
	return filename

#Identify notes in saved audio
def getNotes(filename):

	'''Downsampling factor, makes audio signal smaller by lowering 
		sample rate. Can be changed to downsample by that factor'''
	downsample = 1

	#Sampling rate of file
	samplerate = 44100 // downsample

	'''Fast Fourier Transform: Method of applying several fourier
	transforms to a amplitude vs time graph to convert it into a 
	amp vs freq graph, also known as a spectra plot.
	
	FFT Size affects resolution of end spectra. 
	- Number of lines = 1/2 of FFT Size.
	- Freq resolution of each spectral line: sample rate / FFT Size
	- Larger the size, greater the resolution, but more time needed
	
	Essentially window size of overlapping windows, in terms 
	of samples
	Done in blocks of 2 so the size must be a power of two.
	512 is Default
	'''

	fftSize = 512 // downsample

	'''Hop Size: Overlap factor, number of samples between each window,
	determines overlap.

	How many samples are read at each consecutive call

	= FFT size / overlap factor (default is 2)

	I/O delay = window size - hop size
	
	'''
	hopSize = 256
	
	#Get source class from filename, get the samplerate property
	s = source(filename, samplerate, hopSize)
	samplerate = s.samplerate

	#Initialize notes class with default method, other params
	notes_o = notes("default", fftSize, hopSize, samplerate)

	#Header
	#print("%8s" % "time","[ start","vel","last ]")

	# total number of frames read
	total_frames = 0

	#List to hold final notes
	notesList = []

	#Get samples from source object, run notes functions on them
	while True:
		#Get current sample and number of samples read
		samples, read = s()

		#Get the notes vector using the notes object
		new_note = notes_o(samples)

		#If the notes vector is not blank store + print the note vector
		if (new_note[0] != 0):
			noteArray = new_note
			print(noteArray)
			notesList.append(aubio.midi2note(int(new_note[0])))
		
		total_frames += read

		'''As the source is called repeatedly, towards the end of the
			stream read will become less than hop size. '''
		if read < hopSize:
			return notesList

def getChords(filepath):
	p = Popen("python /Users/Imaan/tensorflow/tensorflow/examples/speech_commands/label_wav.py \
		--graph=/tmp/my_frozen_graph.pb \
		--labels=/tmp/speech_commands_train/conv_labels.txt \
		--wav=" + filepath, 
		stdout=PIPE)

	result = []

	for line in p.stdout:
		result.append(line.decode("utf-8"))

	return result

def getTempo(filename):
	cmd = ["aubio", "tempo", filename, "-r 44100"]
	p = Popen(cmd, shell=True, stdout=PIPE)

	
	bpm = []

	for line in p.stdout:
		bpm.append(line.decode("utf-8"))

	return float(bpm[0].split()[0]) + 17

def onsetDetection(filename):
	win_s = 512                 # fft size
	hop_s = win_s // 2          # hop size

	samplerate = 44100

	s = source(filename, samplerate, hop_s)
	samplerate = s.samplerate

	o = onset("default", win_s, hop_s, samplerate)

	# list of onsets, in samples
	onsets = []

	# total number of frames read
	total_frames = 0

	#Returns onset (frames at which note is heard)
	#SR = frames/sec
	#time * SR = frames
	#time = frames / SR

	while True:
	    samples, read = s()
	    if o(samples):
	        onsets.append(o.get_last())
	    total_frames += read
	    if read < hop_s: 
	    	break

	print(onsets)
	print(len(onsets))

	#All note lengths will be stored here
	notesLen = []

	#Get time between each onset interval (time of each note)
	for i in range(len(onsets)-1):
		frames = onsets[i+1]-onsets[i]
		notesLen.append(frames/44100)
		print(len(notesLen))
		return notesLen

def generateSheet(filename):
	im = Image.open(filename)

	#Get the bpm of the song
	bpm = getTempo(filename)

	#Get the array of note lengths
	noteLens = getTempo(filename)

	#Sort the note lengths into a list
	#Notes[0] = quarter
	#Notes[1] = half
	#Notes[2] = third
	#Notes[3] = whole
	notes = [[],[],[],[]]

	for i in range(len(noteLens)):
		#Check if the note is a quarter note
		quarterNote = 60/bpm
		if math.isclose(i,quarterNote, rel_tol=0.001):
			notes[0].append(i)

		elif math.isclose(i, quarterNote*2,rel_tol=0.001):
			notes[1].append(i)


		elif math.isclose(i, quarterNote*3,rel_tol=0.001):
			notes[2].append(i)


		elif math.isclose(i, quarterNote*4,rel_tol=0.001):
			notes[3].append(i)

def genTabs(notesList):
	tab = [["e|"],
	["B|"],
	["G|"],
	["D|"],
	["A|"],
	["E|"]]

	for i in range(len(notesList)):
		#Add the note positions
		if notesList[i] == "E3":
			tab[0][0] += "2"
		elif notesList[i] == "B3":
			tab[1][0] += "0"
		elif notesList[i] == "G3":
			tab[2][0] += "0"
		elif notesList[i] == "D3":
			tab[3][0] += "0"
	#Fil the rest of the tab with dashes
	#19 total lines in a blank tab
	# - (the number of notes - the starting 2 chars)
	for i in range(6):
		for x in range(19- (len(tab[i])-2) ):
			tab[i][0] += "-"

	return tab
'''
Once a note is detected record it, 
'''
#60/bpm = length of quarter note
print(getChords("C:/Users/Imaan/Music/SampleChords/cChord1.wav"))