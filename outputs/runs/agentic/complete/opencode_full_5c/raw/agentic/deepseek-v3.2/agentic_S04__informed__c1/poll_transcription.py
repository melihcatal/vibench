import boto3
import json
import time
from typing import Dict, Any, Optional


def poll_transcription_job(
    job_name: str, max_wait_seconds: int = 300, poll_interval: int = 5
) -> Dict[str, Any]:
    """
    Poll a transcription job and return the transcript when complete.

    Args:
        job_name: Name of the transcription job
        max_wait_seconds: Maximum time to wait for completion
        poll_interval: Seconds between polling attempts

    Returns:
        Dictionary with transcript text and metadata
    """
    transcribe_client = boto3.client("transcribe")

    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )

        status = response["TranscriptionJob"]["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]

            import urllib.request

            with urllib.request.urlopen(transcript_uri) as url:
                transcript_data = json.loads(url.read().decode())

            transcript_text = transcript_data["results"]["transcripts"][0]["transcript"]

            items = transcript_data["results"].get("items", [])
            speakers = (
                transcript_data["results"].get("speaker_labels", {}).get("segments", [])
            )

            return {
                "job_name": job_name,
                "status": status,
                "transcript": transcript_text,
                "items": items,
                "speakers": speakers,
                "transcript_uri": transcript_uri,
            }

        elif status == "FAILED":
            failure_reason = response["TranscriptionJob"].get(
                "FailureReason", "Unknown error"
            )
            raise Exception(f"Transcription job failed: {failure_reason}")

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Transcription job not completed within {max_wait_seconds} seconds"
    )


def get_transcript_text(job_name: str) -> str:
    """
    Get just the transcript text from a completed job.

    Args:
        job_name: Name of the transcription job

    Returns:
        The transcript text
    """
    result = poll_transcription_job(job_name, max_wait_seconds=0)
    return result["transcript"]
