import azure.cognitiveservices.speech as speechsdk

def stream_microphone():
    speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_started.connect(stop_cb)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('RECOGNIZED: Text={}'.format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print('NOMATCH: Speech could not be recognized.')
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print('CANCELED: Reason={}'.format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print('CANCELED: ErrorCode={}'.format(cancellation_details.error_code))
            print('CANCELED: ErrorDetails={}'.format(cancellation_details.error_details))
            print('CANCELED: Did you update the subscription info?')

if __name__ == '__main__':
    stream_microphone()