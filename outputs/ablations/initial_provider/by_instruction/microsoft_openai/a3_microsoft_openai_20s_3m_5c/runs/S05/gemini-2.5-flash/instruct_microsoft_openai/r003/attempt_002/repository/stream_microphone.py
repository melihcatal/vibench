import azure.cognitiveservices.speech as speechsdk
import os

def stream_microphone_audio():
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"), 
        region=os.environ.get("SPEECH_REGION")
    )
    audio_config = speechsdk.AudioConfig(use_ microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )

    print("Speak into your microphone.")
    
    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(
        lambda evt: print('RECOGNIZED: {}'.format(evt.result.text))
    )
    speech_recognizer.canceled.connect(stop_cb)
    speech_recognizer.session_stopped.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        pass
    speech_recognizer.stop_continuous_recognition()
