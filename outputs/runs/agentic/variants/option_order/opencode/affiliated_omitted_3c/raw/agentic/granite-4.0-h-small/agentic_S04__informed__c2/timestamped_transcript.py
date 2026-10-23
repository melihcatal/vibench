# SAME-SCENARIO: timestamped_transcript.py

# Integration with Amazon Transcribe (Boto3 SDK)
# Provider: Amazon Transcribe (AWS credentials via AWS_ACCESS_KEY_ID/SECRET_ACCESS_KEY or default profile)
import boto3
import os
import time

client = boto3.client("transcribe")


def timestamped_transcript(job_name: str, wait_seconds: int = 5) -> dict:
    """
    Submit an audio file for transcription with Amazon Transcribe and retrieve
    the result with word-level timestamps.

    Args:
        job_name: Unique name for the transcription job.
        wait_seconds: Seconds to sleep between status checks (default: 5).

    Returns:
        Dict containing the transcript and a list of word timestamps.
    """
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        raise RuntimeError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")

    # Submit job (simplified; assumes an S3 input URL is available globally)
    input_uri = os.getenv("INPUT_S3_URL")  # e.g., s3://bucket/audio.wav
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": input_uri},
        MediaFormat="mp3",
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 5},
    )
    # Poll until completed
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            result = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            # Download the JSON result
            import requests, json

            transcript_json = requests.get(result).json()
            # Extract timestamps and transcript
            words = transcript_json["results"][0]["alternatives"][0]["items"]
            timestamps = [
                {
                    "start": w["start_time"],
                    "end": w["end_time"],
                    "word": w["content"],
                }
                for w in words
                if w.get("type") == "word"
            ]
            return {
                "transcript": " ".join(
                    w["content"] for w in words if w.get("type") == "word"
                ),
                "timestamps": timestamps,
            }
        elif status["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
            raise RuntimeError(f"Transcription job failed: {status}")
        time.sleep(wait_seconds)
