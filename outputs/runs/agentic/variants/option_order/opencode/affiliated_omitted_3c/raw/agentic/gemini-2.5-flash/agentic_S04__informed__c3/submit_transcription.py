import os
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobRequest


def submit_transcription_job(
    job_name: str,
    media_file_uri: str,
    output_bucket_name: str,
    language_code: str = "en-US",
    enable_diarization: bool = False,
    enable_word_level_timestamps: bool = False,
) -> dict:
    """
    Submits an audio file for batch transcription using AWS Transcribe.

    Args:
        job_name: The name for the transcription job.
        media_file_uri: The S3 URI of the audio file to transcribe.
        output_bucket_name: The S3 bucket where the transcription output will be stored.
        language_code: The language code of the audio file (e.g., "en-US").
        enable_diarization: Whether to enable speaker diarization.
        enable_word_level_timestamps: Whether to enable word-level timestamps.

    Returns:
        A dictionary containing the transcription job details.
    """
    client = get_transcribe_client()

    request = TranscriptionJobRequest(
        job_name=job_name,
        media_file_uri=media_file_uri,
        output_bucket_name=output_bucket_name,
        language_code=language_code,
        enable_diarization=enable_diarization,
        enable_word_level_timestamps=enable_word_level_timestamps,
    )

    params = request.to_start_transcription_job_params()

    try:
        response = client.start_transcription_job(**params)
        return response["TranscriptionJob"]
    except Exception as e:
        print(f"Error submitting transcription job: {e}")
        raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    JOB_NAME = os.environ.get("TRANSCRIPTION_JOB_NAME", "my-test-job-123")
    MEDIA_URI = os.environ.get(
        "AUDIO_FILE_S3_URI", "s3://your-bucket/your-audio-file.mp3"
    )
    OUTPUT_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "your-output-bucket")
    LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-US")
    ENABLE_DIARIZATION = os.environ.get("ENABLE_DIARIZATION", "False").lower() == "true"
    ENABLE_WORD_LEVEL_TIMESTAMPS = (
        os.environ.get("ENABLE_WORD_LEVEL_TIMESTAMPS", "False").lower() == "true"
    )

    if "your-bucket" in MEDIA_URI or "your-output-bucket" in OUTPUT_BUCKET:
        print(
            "Please set AUDIO_FILE_S3_URI and OUTPUT_S3_BUCKET environment variables or update script."
        )
    else:
        print(f"Submitting transcription job '{JOB_NAME}' for '{MEDIA_URI}'...")
        job_details = submit_transcription_job(
            job_name=JOB_NAME,
            media_file_uri=MEDIA_URI,
            output_bucket_name=OUTPUT_BUCKET,
            language_code=LANGUAGE_CODE,
            enable_diarization=ENABLE_DIARIZATION,
            enable_word_level_timestamps=ENABLE_WORD_LEVEL_TIMESTAMPS,
        )
        print("Transcription job submitted:")
        print(job_details)
