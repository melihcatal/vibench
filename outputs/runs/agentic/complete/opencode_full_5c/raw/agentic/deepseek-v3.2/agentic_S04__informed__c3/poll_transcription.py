import os
import time
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription(job_id: str, max_wait_seconds: int = 300) -> TranscriptionResult:
    """
    Poll a transcription job and return the transcript.

    Args:
        job_id: Transcription job ID
        max_wait_seconds: Maximum time to wait for completion

    Returns:
        TranscriptionResult object with transcript and metadata
    """
    client = get_speech_client()

    start_time = time.time()
    poll_interval = 5  # seconds

    while time.time() - start_time < max_wait_seconds:
        try:
            response = client.get_transcription_job(TranscriptionJobName=job_id)
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]

            if status == "COMPLETED":
                # Get the transcript from the S3 URI
                transcript_uri = response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]

                # Download transcript from S3
                import json
                import urllib.request

                transcript_data = json.loads(
                    urllib.request.urlopen(transcript_uri).read()
                )
                transcript_text = transcript_data["results"]["transcripts"][0][
                    "transcript"
                ]

                # Extract speaker labels if available
                speaker_segments = []
                if "speaker_labels" in transcript_data["results"]:
                    for segment in transcript_data["results"]["speaker_labels"][
                        "segments"
                    ]:
                        speaker_segments.append(
                            {
                                "speaker": segment["speaker_label"],
                                "start_time": float(segment["start_time"]),
                                "end_time": float(segment["end_time"]),
                                "items": [],
                            }
                        )

                # Extract word timestamps if available
                word_timestamps = []
                if "items" in transcript_data["results"]:
                    for item in transcript_data["results"]["items"]:
                        if item["type"] == "pronunciation":
                            word_timestamps.append(
                                {
                                    "word": item["alternatives"][0]["content"],
                                    "start_time": float(item["start_time"]),
                                    "end_time": float(item["end_time"]),
                                    "confidence": float(
                                        item["alternatives"][0]["confidence"]
                                    ),
                                }
                            )

                return TranscriptionResult(
                    job_id=job_id,
                    transcript=transcript_text,
                    language_code=response["TranscriptionJob"]["LanguageCode"],
                    speaker_segments=speaker_segments,
                    word_timestamps=word_timestamps,
                    raw_response=transcript_data,
                )

            elif status == "FAILED":
                failure_reason = response["TranscriptionJob"].get(
                    "FailureReason", "Unknown error"
                )
                raise Exception(f"Transcription job failed: {failure_reason}")

            # Job is still in progress
            time.sleep(poll_interval)

        except ClientError as e:
            print(f"Error polling transcription job: {e}")
            raise

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {max_wait_seconds} seconds"
    )


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        result = poll_transcription(sys.argv[1])
        print(f"Transcript: {result.transcript}")
    else:
        print("Usage: python poll_transcription.py <job_id>")
