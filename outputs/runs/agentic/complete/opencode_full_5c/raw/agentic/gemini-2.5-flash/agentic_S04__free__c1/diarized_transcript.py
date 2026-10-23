import os
from google.cloud import speech_v1p1beta1 as speech


def request_diarized_transcript(
    gcs_uri: str, project_id: str, sample_rate_hertz: int, language_code: str
):
    """Requests speaker diarization for a recorded meeting.

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
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Example: Expecting 2 speakers
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name


if __name__ == "__main__":
    # Example usage (replace with actual values)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    gcs_uri = "gs://cloud-samples-data/speech/flac/commercial_mono.flac"  # Use an audio file suitable for diarization
    sample_rate_hertz = 16000
    language_code = "en-US"

    if project_id:
        print(f"Submitting diarization job for {gcs_uri}...")
        operation_name = request_diarized_transcript(
            gcs_uri, project_id, sample_rate_hertz, language_code
        )
        print(f"Diarization job submitted. Operation Name: {operation_name}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
