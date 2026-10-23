from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer

def transcribe_audio(audio_data):
    speech_config = SpeechConfig(subscription='YOUR_AZURE_SPEECH_KEY', region='YOUR_AZURE_SPEECH_REGION')
    audio_config = speechconfig.audio_config(filename=audio_data)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    return result.text