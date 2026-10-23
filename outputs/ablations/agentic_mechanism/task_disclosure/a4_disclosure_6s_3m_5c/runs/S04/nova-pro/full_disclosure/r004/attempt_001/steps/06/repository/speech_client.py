from google.cloud import speech_v1p1beta1 as speech

def create_client():
    return speech.SpeechClient()

def get_config(language_code='en-US', sample_rate_hertz=16000, encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16):
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code
    )
    return config

def get_audio(file_path):
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    return audio