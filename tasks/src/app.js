import "./sass/app.scss"
import $ from 'jquery';
import "popper.js"

window.jQuery = $;
window.$ = $;
import "bootstrap"

import select2 from 'select2';
import 'select2/dist/css/select2.css';


var $elm = $('#js-task-voice-notes');

        function load_voice_notes() {
            $elm.html("<h5>Loading ...</h5>")
            var url = '/task_voice_notes/' + $elm.data('task-id')
            $.get(url, function (data) {
                $elm.html(data.view)
            });
        }

        function startRecording() {
            let constraints = {audio: true, video: false}
            recordButton.disabled = true;
            stopButton.disabled = false;
            pauseButton.disabled = false;

            navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
                audioContext = new AudioContext();
                document.getElementById("formats").innerHTML = "Format: 1 channel pcm @ " + audioContext.sampleRate / 1000 + "kHz"
                gumStream = stream;
                input = audioContext.createMediaStreamSource(stream);
                rec = new Recorder(input, {numChannels: 1})
                rec.record()
            }).catch(function (err) {
                recordButton.disabled = false;
                stopButton.disabled = true;
                pauseButton.disabled = true
            });
        }
        function pauseRecording(e) {
            e.preventDefault();
            console.log("pauseButton clicked rec.recording=", rec.recording);
            if (rec.recording) {
                rec.stop();
                pauseButton.innerHTML = "Resume";
            } else {
                rec.record()
                pauseButton.innerHTML = "Pause";
            }
        }
        function stopRecording() {
            stopButton.disabled = true;
            recordButton.disabled = false;
            pauseButton.disabled = true;
            pauseButton.innerHTML = "Pause";
            rec.stop();
            gumStream.getAudioTracks()[0].stop();
            rec.exportWAV(createDownloadLink);
        }


        function delete_voice_note(id){
            if (confirm('Are you sure to delete the voice note?')){
                 $.get('/delete_voice_note/'+id,function (data){
                     if(data.success){
                         load_voice_notes();
                     }else{
                         alert('Failed to delete the task');
                     }
                });
            }
        }


        function createDownloadLink(blob) {
            let url = URL.createObjectURL(blob);
            let au = document.createElement('audio');
            let li = document.createElement('li');
            let link = document.createElement('a');
            let filename = new Date().toISOString();

            au.controls = true;
            au.src = url;

            link.href = url;
            link.download = filename + ".wav";
            link.innerHTML = "Save to disk";

            li.appendChild(au);

            let deletebtn = document.createElement('a')
            deletebtn.href = "javascript:void(0);";
            deletebtn.innerHTML = "Delete"
            deletebtn.setAttribute('class', 'btn btn-danger')
            deletebtn.addEventListener('click', function(e){
                e.preventDefault();
                e.target.parentNode.remove();
            });
            li.appendChild(deletebtn)

            let upload = document.createElement('a');
            upload.href = "javascript:void(0);";
            upload.setAttribute('class', 'btn btn-primary')
            upload.innerHTML = "Upload";



            upload.addEventListener("click", function (event) {
                let fd = new FormData();
                fd.append("voice_memo", blob, filename);
                $.ajax({
                    type: "POST",
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        $('.add-note-loader').css("visibility", "visible");
                    },
                    url: '/add_voice_note/'+$elm.data('task-id'),
                    data: fd,
                    success: function (data) {
                        $('.add-note-loader').css("visibility", "hidden");
                        recordingsList.innerHTML = "";
                        load_voice_notes()
                    },
                    error: function (request, status, error) {
                        $('.add-note-loader').css("visibility", "hidden");
                        alert('Something went wrong!');
                    },
                    complete: function () {
                        $('.add-note-loader').css("visibility", "hidden");
                    }
                });
            })
            li.appendChild(document.createTextNode(" "))
            li.appendChild(upload)
            recordingsList.appendChild(li);
        }


        $(function(){
           load_voice_notes();
           URL = window.URL || window.webkitURL;
            let gumStream;                      //stream from getUserMedia()
            let rec;                            //Recorder.js object
            let input;                          //MediaStreamAudioSourceNode we'll be recording
            let AudioContext = window.AudioContext || window.webkitAudioContext;
            let audioContext //audio context to help us record

            let recordButton = document.getElementById("recordButton");
            let stopButton = document.getElementById("stopButton");
            let pauseButton = document.getElementById("pauseButton");
            recordButton && recordButton.addEventListener("click", startRecording);
            stopButton && stopButton.addEventListener("click", stopRecording);
            pauseButton && pauseButton.addEventListener("click", pauseRecording);

            $('body').on('click', '.detete-note', function(){
                delete_voice_note($(this).data('recording-id'))
            });
        });


