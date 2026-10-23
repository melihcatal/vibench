import os
import time

from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import TranscriptionConfig

def submit_transcription_job(audio_uri: str, language_code: str = "en-US") -> str:
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        audio_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The language of the audio file (e.g., "en-US").

    Returns:
        The operation name of the transcription job.
    """
    client = get_speech_client()

    config_obj = TranscriptionConfig(audio_uri=audio_uri, language_code=language_code)
    config = config_obj.to_recognition_config()
    audio = config_obj.to_recognition_audio()

    try:
        # Google Cloud Speech-to-Text API Call
        # Model ID identifiable by "model": "default" (or others like "latest_long") in config
        operation = client.long_running_recognize(config=config, audio=audio)
        print(f"Transcription job submitted. Operation name: {operation.operation.name}")
        return operation.operation.name
    except GoogleAPIError as e:
        print(f"Error submitting transcription job: {e}")
        raise

if __name__ == '__main__':
    # Example usage (replace with a real GCS URI if running)
    # Make sure GOOGLE_APPLICATION_CREDENTIALS is set up
    gcs_audio_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    try:
        op_name = submit_transcription_job(gcs_audio_uri)
        print(f"Operation Name: {op_name}")
    except Exception as e:
        print(f"Failed to submit job: {e}")
