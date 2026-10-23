from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import os

def submit_transcription_job(gcs_uri: str, language_code: str = "en-US"):
    """
    Submits an audio file for batch transcription to Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, # Example, adjust based on actual audio
        sample_rate_hertz=16000, # Example, adjust based on actual audio
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(request={"config": config, "audio": audio})
    print(f"Transcription operation submitted: {operation.operation.name}")
    return operation.operation.name
