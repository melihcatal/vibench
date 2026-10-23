import os
import sys
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionConfig, TranscriptionAudio


def submit_transcription_job(gcs_uri: str, language_code: str = "en-US") -> str:
    """
    Submits an audio file for batch transcription to Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://bucket/audio.flac").
        language_code: The language code for the audio (e.g., "en-US").

    Returns:
        The name of the long-running operation.
    """
    client = SpeechClient()
    audio = TranscriptionAudio(uri=gcs_uri)
    config = TranscriptionConfig(language_code=language_code)

    # The actual submission happens here
    operation = client.submit_long_running_recognize(audio, config)
    print(
        f"Submitted transcription job for {gcs_uri}. Operation name: {operation.operation_id}"
    )
    return operation.operation_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <gcs_uri> [language_code]")
        sys.exit(1)

    gcs_uri = sys.argv[1]
    language_code = sys.argv[2] if len(sys.argv) > 2 else "en-US"

    # For demonstration, ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    operation_name = submit_transcription_job(gcs_uri, language_code)
    print(f"Operation ID: {operation_name}")
