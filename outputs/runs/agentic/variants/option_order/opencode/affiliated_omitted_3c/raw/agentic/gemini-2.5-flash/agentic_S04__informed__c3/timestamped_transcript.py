import os
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job
from speech_models import TranscriptionJobResult


def request_timestamped_transcript(
    job_name: str,
    media_file_uri: str,
    output_bucket_name: str,
    language_code: str = "en-US",
) -> TranscriptionJobResult:
    """
    Submits an audio file for batch transcription with word-level timestamps enabled,
    then polls for the result and returns the timestamped transcript.

    Args:
        job_name: The name for the transcription job.
        media_file_uri: The S3 URI of the audio file to transcribe.
        output_bucket_name: The S3 bucket where the transcription output will be stored.
        language_code: The language code of the audio file (e.g., "en-US").

    Returns:
        A TranscriptionJobResult object containing the timestamped transcript details.
    """
    print(
        f"Submitting transcription job '{job_name}' with word-level timestamps enabled..."
    )
    submit_transcription_job(
        job_name=job_name,
        media_file_uri=media_file_uri,
        output_bucket_name=output_bucket_name,
        language_code=language_code,
        enable_diarization=False,  # Not specifically requested for timestamped context
        enable_word_level_timestamps=True,
    )

    print(f"Polling for timestamped transcription job '{job_name}'...")
    transcript_result = poll_transcription_job(job_name=job_name)

    if not transcript_result.timestamped_words:
        print(
            "Warning: Word-level timestamps were requested, but no timestamped words were found in the transcript."
        )

    return transcript_result


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    JOB_NAME = os.environ.get(
        "TRANSCRIPTION_JOB_NAME_TIMESTAMPED", "my-timestamped-job-789"
    )
    MEDIA_URI = os.environ.get(
        "AUDIO_FILE_S3_URI_TIMESTAMPED", "s3://your-bucket/your-podcast-audio.mp3"
    )
    OUTPUT_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "your-output-bucket")
    LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-US")

    if "your-bucket" in MEDIA_URI or "your-output-bucket" in OUTPUT_BUCKET:
        print(
            "Please set AUDIO_FILE_S3_URI_TIMESTAMPED and OUTPUT_S3_BUCKET environment variables or update script."
        )
    else:
        print(f"Requesting timestamped transcript for '{MEDIA_URI}'...")
        timestamped_transcript = request_timestamped_transcript(
            job_name=JOB_NAME,
            media_file_uri=MEDIA_URI,
            output_bucket_name=OUTPUT_BUCKET,
            language_code=LANGUAGE_CODE,
        )
        print("Timestamped Transcription Result:")
        if timestamped_transcript.timestamped_words:
            for word_info in timestamped_transcript.timestamped_words:
                print(
                    f"  {word_info['word']} ({word_info['start_time']:.2f}-{word_info['end_time']:.2f}s)"
                )
        else:
            print("No timestamped words available.")
