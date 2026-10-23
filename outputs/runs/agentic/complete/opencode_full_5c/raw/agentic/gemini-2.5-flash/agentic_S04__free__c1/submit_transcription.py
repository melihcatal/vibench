import os
from google.cloud import speech_v1p1beta1 as speech


def submit_transcription_job(
    gcs_uri: str, project_id: str, sample_rate_hertz: int, language_code: str
):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        project_id: The Google Cloud project ID.
        sample_rate_hertz: The sample rate of the audio in Hertz.
        language_code: The language code for the audio (e.g., "en-US").

    Returns:
        The operation name of the long-running transcription job.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name


if __name__ == "__main__":
    # Example usage (replace with actual values)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    gcs_uri = "gs://cloud-samples-data/speech/flac/commercial_mono.flac"
    sample_rate_hertz = 16000
    language_code = "en-US"

    if project_id:
        print(f"Submitting transcription job for {gcs_uri}...")
        operation_name = submit_transcription_job(
            gcs_uri, project_id, sample_rate_hertz, language_code
        )
        print(f"Transcription job submitted. Operation Name: {operation_name}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
