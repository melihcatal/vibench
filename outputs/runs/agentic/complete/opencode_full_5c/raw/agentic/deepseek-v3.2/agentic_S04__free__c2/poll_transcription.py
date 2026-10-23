import time
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription(job_id: str, timeout_seconds: int = 300) -> TranscriptionResult:
    """
    Poll a transcription job and return the transcript.

    Args:
        job_id: Transcription job ID
        timeout_seconds: Maximum time to wait for completion

    Returns:
        TranscriptionResult object containing the transcript
    """
    client = get_speech_client()

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            response = client.get_transcription_job(TranscriptionJobName=job_id)
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]

            if status == "COMPLETED":
                # Get the transcript from the output URI
                transcript_uri = response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]

                # Download and parse the transcript
                import json
                import urllib.request

                transcript_data = json.loads(
                    urllib.request.urlopen(transcript_uri).read()
                )
                transcript_text = transcript_data["results"]["transcripts"][0][
                    "transcript"
                ]

                # Extract items if available
                items = []
                if "items" in transcript_data["results"]:
                    items = transcript_data["results"]["items"]

                # Extract speaker labels if available
                speaker_labels = []
                if "speaker_labels" in transcript_data["results"]:
                    speaker_labels = transcript_data["results"]["speaker_labels"][
                        "segments"
                    ]

                return TranscriptionResult(
                    job_id=job_id,
                    transcript=transcript_text,
                    items=items,
                    speaker_labels=speaker_labels,
                    status="COMPLETED",
                )

            elif status == "FAILED":
                failure_reason = response["TranscriptionJob"].get(
                    "FailureReason", "Unknown error"
                )
                raise Exception(f"Transcription job failed: {failure_reason}")

            else:
                # Job is still in progress
                time.sleep(5)

        except ClientError as e:
            print(f"Error polling transcription job: {e}")
            raise

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {timeout_seconds} seconds"
    )
