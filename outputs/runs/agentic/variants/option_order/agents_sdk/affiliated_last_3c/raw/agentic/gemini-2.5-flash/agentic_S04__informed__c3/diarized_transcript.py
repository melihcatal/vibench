from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import os

def request_diarized_transcript(gcs_uri: str, language_code: str = "en-US"):
    """
    Requests speaker diarization for a recorded meeting using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, # Example, adjust based on actual audio
        sample_rate_hertz=16000, # Example, adjust based on actual audio
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=2, # Example, specify the expected number of speakers
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(request={"config": config, "audio": audio})
    print(f"Diarization operation submitted: {operation.operation.name}")
    
    # In a real scenario, you'd poll this operation similar to poll_transcription.py
    # For this example, we just return the operation name.
    return operation.operation.name
