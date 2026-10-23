from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import storage
import os

def submit_transcription_job(gcs_uri: str, project_id: str):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://your-bucket/audio.flac").
        project_id: Your Google Cloud project ID.
    
    Returns:
        The operation name for the long-running transcription job.
    """
    client = speech.SpeechClient()

    audio = {"uri": gcs_uri}
    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(f"Transcription operation started: {operation.operation.name}")
    return operation.operation.name

if __name__ == '__main__':
    # Example usage (replace with your actual GCS URI and project ID)
    GCS_URI = os.getenv("GCS_AUDIO_URI", "gs://cloud-samples-data/speech/brooklyn_bridge.flac")
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    
    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        submit_transcription_job(GCS_URI, PROJECT_ID)
