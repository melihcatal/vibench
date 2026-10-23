from google.cloud import speech_v1p1beta1 as speech

def create_client():
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    client = speech.SpeechClient()
    return client, streaming_config