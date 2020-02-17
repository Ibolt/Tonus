from django.urls import path
from . import views

#Namespacing of urls
app_name = 'main'

#URL Paths for the controller to navigate
urlpatterns = [
	#Path will point to homepage view
	path("", views.home, name="Home"),
	path("notes/", views.notes, name="notes"),
	path("chords/", views.chords, name="chords"),
	path("recording/", views.recording, name="recording"),
	]