from speech_client import get_speech_client
from google.cloud import speech_v1p1beta1 as speech

def submit_transcription_job(gcs_uri: str, language_code: str = "en-US"):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The language of the audio file.

    Returns:
        The long-running operation for the transcription job.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code=language_code,
    )

    operation = client.longrunning_recognize(config=config, audio=audio)
    print(f"Transcription job submitted. Operation name: {operation.operation.name}")
    return operation
