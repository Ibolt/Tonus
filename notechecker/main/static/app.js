URL = window.URL || window.webkitURL;

//Stream from getUserMedia()
var gumStream;

//Recorder.js object
var rec;

//MediaStreamAudioSourceNode we will record
var input;

//Shim (API call intercept) for AudioContext when not avb
var AudioContext = window.AudioContext || window.webkitAudioContext;

//New Audio Context to help record
var audioContext = new AudioContext;

//Get buttons and add events
var recordBt = document.getElementById("recordBt");
var stopBt = document.getElementById("stopBt");
var pauseBt = document.getElementById("pauseBt");

/*
Launches promise based on getUserMedia()
On success passes audio stream to audio context.
*/

function startRecording() {
	var constraints = {
		audio: true,
		video: false
	}

	//Disable button until we get response from getUserMedia()
	recordBt.disabled = true;
	stopBt.disabled = false;
	pauseBt.disabled = false;

	//Using getUserMedia()
	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		//Assign to gumStream for use later
		gumStream = stream;

		//Use Stream
		input = audioContext.createMediaStreamSource(stream);

		//Create recorder object and configure to record mono
		rec = new Recorder(input, {
			numChannels: 1
		})

		rec.record();
	}).catch(function(err) {
		//enable record button if getUserMedia() fails
		recordBt.disabled = false;
		stopBt.disabled = true;
		pauseBt.disabled = true;
	});
}

function pauseRecording() {
	if (rec.recording) {
		rec.stop();
		pauseBt.innerHTML = "Resume";
	}
	else {
		rec.record()
		pauseBt.innerHTML = "Pause";
	}
}

function stopRecording() {
	stopBt.disabled = true;
	recordBt.disabled = false;
	pauseBt.disabled = false;

	//Reset button in case recording stopped while paused
	pauseBt.innerHTML = "Pause";

	rec.stop();
	gumStream.getAudioTracks()[0].stop();

	//Create wav blob, pass to link
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	var url = URL.createObjectURL(blob);
	var au = document.getElementById("au");
	var link = document.getElementById("link");

	au.controls = true;
	au.src = url;

	//Link a element to blob
	link.href = url;
	link.download = "recording.wav";
}