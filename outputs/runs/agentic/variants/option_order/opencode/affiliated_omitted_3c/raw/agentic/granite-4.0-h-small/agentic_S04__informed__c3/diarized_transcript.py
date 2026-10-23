# Amazon Transcribe integration with speaker diarization
import os
import boto3

# Use the same client as submit_transcription.py
TRANSCRIBE = boto3.client(
    "transcribe",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def request_diarized_transcript(
    job_name,
    audio_file_uri,
    language_code="en-US",
    vocab_name=None,
    diarization_config=None,
):
    """Submit a transcription job with speaker diarization enabled.
    diarization_config: dict with 'MaxSpeakers' field, e.g. {'MaxSpeakers': 5}
    Returns the job name for polling.
    """
    TRANSCRIBE.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        Media={"MediaFileUri": audio_file_uri},
        MediaFormat="mp3",  # adjust as needed
        Settings={
            # Optional vocabulary
            "VocabularyName": vocab_name,
            # Required diarization config
            "DiarizationConfig": diarization_config,
        },
    )
    return job_name
