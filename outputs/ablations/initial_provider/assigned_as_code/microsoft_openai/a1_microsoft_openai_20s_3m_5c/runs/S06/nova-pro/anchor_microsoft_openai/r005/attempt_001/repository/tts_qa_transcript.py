import azure.cognitiveservices.speech as speechsdk

def transcribe_audio(audio_bytes):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioConfig(filename=None)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        raise RuntimeError('Azure speech recognition failed')