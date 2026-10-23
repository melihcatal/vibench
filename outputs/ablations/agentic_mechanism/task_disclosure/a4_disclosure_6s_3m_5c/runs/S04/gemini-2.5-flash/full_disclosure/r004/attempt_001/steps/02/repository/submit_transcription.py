import os
from google.cloud import speech_v1p1beta1 as speech

def submit_transcription_job(gcs_uri: str, project_id: str, audio_channel_count: int = 1):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        project_id: The Google Cloud project ID.
        audio_channel_count: The number of audio channels in the recording.

    Returns:
        The operation name of the long-running transcription job.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        diarization_speaker_count=audio_channel_count,
        model="video",  # Use the video model for better accuracy with meeting recordings
    )

    # Set the output GCS URI for the transcription results
    output_config = speech.TranscriptOutputConfig(gcs_uri=f"gs://{os.getenv("GCS_BUCKET_NAME", "your-gcs-bucket")}/transcription_output/")

    # Asynchronous transcription
    operation = client.long_running_recognize(
        config=config,
        audio=audio,
        output_config=output_config,
    )

    return operation.operation.name
