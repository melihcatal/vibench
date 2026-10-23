import azure.cognitiveservices.speech as speechsdk

def transcribe_audio(audio_file):
    speech_config = speechsdk.SpeechConfig(subscription='AZURE_SPEECH_KEY', region='AZURE_SPEECH_REGION')
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text