from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from speech_client import get_speech_client

def submit_transcription_job(gcs_uri: str, language_code: str = "en-US"):
    """
    Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The language of the audio file.

    Returns:
        The long-running operation object.
    """
    client = get_speech_client()

    audio = speech_v1p1beta1.types.RecognitionAudio(uri=gcs_uri)
    config = speech_v1p1beta1.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC, # Assuming FLAC, adjust as needed
        sample_rate_hertz=16000, # Adjust as needed
        language_code=language_code,
        model="latest_long", # Use a long-form model for batch processing
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(f"Transcription operation submitted: {operation.operation.name}")
    return operation
