import azure.cognitiveservices.speech as speechsdk

def partial_results():
    speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
    audio_config = speechsdk.audio.AudioConfig(filename="YOUR_AUDIO_FILE")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED: {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {}'.format(evt)))

    result = speech_recognizer.start_continuous_recognition_once_async()
    result.get()