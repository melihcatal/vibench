import os
import boto3
from speech_client import SpeechClient

# Amazon Transcribe example with timestamps
client = SpeechClient(service="Amazon Transcribe")


def get_timestamped_transcript(job_id: str):
    """Retrieve a completed transcription with word/segment timestamps.

    Args:
        job_id (str): Transcription job ID.

    Returns:
        list[dict]: List of timestamped words with start/end times and confidence.
    """
    response = client.get_transcription_job(job_id=job_id)
    items = response.get("TranscriptionJob").get("Transcript").get("Items", [])
    timestamped = []
    for item in items:
        timestamped.append(
            {
                "start_time": item.get("StartTimestamp"),
                "end_time": item.get("EndTimestamp"),
                "confidence": item.get("Confidence"),
                "alternatives": [
                    alt.get("Transcript") for alt in item.get("Alternatives", [])
                ],
            }
        )
    return timestamped
