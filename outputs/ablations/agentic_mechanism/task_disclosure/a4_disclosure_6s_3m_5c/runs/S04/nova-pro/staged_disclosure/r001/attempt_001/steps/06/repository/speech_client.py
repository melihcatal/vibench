from google.cloud import speech_v1p1beta1 as speech

def create_speech_client(project_id: str):
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    client = speech.SpeechClient()
    return client, config
