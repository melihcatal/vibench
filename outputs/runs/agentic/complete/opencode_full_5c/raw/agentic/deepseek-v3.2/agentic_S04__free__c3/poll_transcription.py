import json
import time
import boto3
from botocore.exceptions import ClientError
import requests
from speech_client import get_speech_client
from speech_models import TranscriptionResult, TranscriptSegment


def poll_transcription(job_id: str, timeout_seconds: int = 300) -> TranscriptionResult:
    """
    Poll a transcription job and return the transcript when complete.

    Args:
        job_id: Transcription job ID
        timeout_seconds: Maximum time to wait for completion

    Returns:
        TranscriptionResult with transcript text and metadata
    """
    client = get_speech_client()

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            response = client.get_transcription_job(TranscriptionJobName=job_id)
            job = response["TranscriptionJob"]
            status = job["TranscriptionJobStatus"]

            if status == "COMPLETED":
                transcript_uri = job["Transcript"]["TranscriptFileUri"]
                transcript_data = fetch_transcript_from_uri(transcript_uri)

                segments = []
                if "items" in transcript_data.get("results", {}):
                    for item in transcript_data["results"]["items"]:
                        if item["type"] == "pronunciation":
                            segments.append(
                                TranscriptSegment(
                                    text=item["alternatives"][0]["content"],
                                    start_time=float(item["start_time"]),
                                    end_time=float(item["end_time"]),
                                    confidence=float(
                                        item["alternatives"][0].get("confidence", 0.0)
                                    ),
                                )
                            )

                return TranscriptionResult(
                    job_id=job_id,
                    status=status,
                    transcript_text=transcript_data.get("results", {})
                    .get("transcripts", [{}])[0]
                    .get("transcript", ""),
                    segments=segments,
                    language_code=job.get("LanguageCode", "en-US"),
                    completed_at=job.get("CompletionTime"),
                )

            elif status == "FAILED":
                failure_reason = job.get("FailureReason", "Unknown failure")
                raise Exception(f"Transcription job failed: {failure_reason}")

            time.sleep(5)

        except ClientError as e:
            raise Exception(f"AWS Transcribe error: {e.response['Error']['Message']}")

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {timeout_seconds} seconds"
    )


def fetch_transcript_from_uri(uri: str) -> dict:
    """
    Fetch transcript JSON from S3 URI.
    """
    try:
        response = requests.get(uri, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch transcript from {uri}: {e}")
