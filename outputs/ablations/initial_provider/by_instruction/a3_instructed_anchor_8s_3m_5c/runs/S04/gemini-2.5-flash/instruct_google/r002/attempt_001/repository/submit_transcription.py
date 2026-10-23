from speech_client import get_speech_client
from google.cloud import speech_v1p1beta1 as speech

def submit_transcription_job(gcs_uri: str, language_code: str = "en-US"):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://bucket-name/audio.flac").
        language_code: The language of the audio file.

    Returns:
        The operation object from the Google Cloud Speech-to-Text API.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,  # Example encoding
        sample_rate_hertz=16000,  # Example sample rate
        language_code=language_code,
        # A model must be specified to use diarization and word-level timestamps
        model="video", # or "default", "phone_call", "command_and_search"
        use_enhanced=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(f"Transcription job submitted. Operation name: {operation.operation.name}")
    return operation
