import os
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job
from speech_models import TranscriptionJobResult


def request_diarized_transcript(
    job_name: str,
    media_file_uri: str,
    output_bucket_name: str,
    language_code: str = "en-US",
) -> TranscriptionJobResult:
    """
    Submits an audio file for batch transcription with speaker diarization enabled,
    then polls for the result and returns the diarized transcript.

    Args:
        job_name: The name for the transcription job.
        media_file_uri: The S3 URI of the audio file to transcribe.
        output_bucket_name: The S3 bucket where the transcription output will be stored.
        language_code: The language code of the audio file (e.g., "en-US").

    Returns:
        A TranscriptionJobResult object containing the diarized transcript details.
    """
    print(f"Submitting transcription job '{job_name}' with diarization enabled...")
    submit_transcription_job(
        job_name=job_name,
        media_file_uri=media_file_uri,
        output_bucket_name=output_bucket_name,
        language_code=language_code,
        enable_diarization=True,
        enable_word_level_timestamps=False,  # Not specifically requested for diarization context
    )

    print(f"Polling for diarized transcription job '{job_name}'...")
    transcript_result = poll_transcription_job(job_name=job_name)

    if not transcript_result.diarized_segments:
        print(
            "Warning: Diarization was requested, but no speaker labels were found in the transcript."
        )

    return transcript_result


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    JOB_NAME = os.environ.get("TRANSCRIPTION_JOB_NAME_DIARIZED", "my-diarized-job-456")
    MEDIA_URI = os.environ.get(
        "AUDIO_FILE_S3_URI_DIARIZED", "s3://your-bucket/your-meeting-audio.mp3"
    )
    OUTPUT_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "your-output-bucket")
    LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-US")

    if "your-bucket" in MEDIA_URI or "your-output-bucket" in OUTPUT_BUCKET:
        print(
            "Please set AUDIO_FILE_S3_URI_DIARIZED and OUTPUT_S3_BUCKET environment variables or update script."
        )
    else:
        print(f"Requesting diarized transcript for '{MEDIA_URI}'...")
        diarized_transcript = request_diarized_transcript(
            job_name=JOB_NAME,
            media_file_uri=MEDIA_URI,
            output_bucket_name=OUTPUT_BUCKET,
            language_code=LANGUAGE_CODE,
        )
        print("Diarized Transcription Result:")
        if diarized_transcript.diarized_segments:
            for segment in diarized_transcript.diarized_segments:
                print(
                    f"  [Speaker {segment['speaker']} ({segment['start_time']:.2f}-{segment['end_time']:.2f}s)]: {segment['text']}"
                )
        else:
            print("No diarized segments available.")
