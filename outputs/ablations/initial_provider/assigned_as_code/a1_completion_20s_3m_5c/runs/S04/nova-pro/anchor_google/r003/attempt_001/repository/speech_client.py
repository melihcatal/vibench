from google.cloud import speech

def get_speech_client():
    return speech.SpeechClient()

def get_recognition_config(language_code):
    return speech.RecognitionConfig(language_code=language_code)

def get_recognition_audio(uri):
    return speech.RecognitionAudio(uri=uri)