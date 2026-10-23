from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

def submit_transcription_job(gcs_uri: str, audio_channel_count: int = 1):
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Example, adjust based on actual audio
        sample_rate_hertz=16000, # Example, adjust based on actual audio
        language_code="en-US",
        audio_channel_count=audio_channel_count,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name
