import os
import boto3
from speech_client import get_speech_client
import json


def archive_summary(job_name):
    """Generate a concise summary of a completed transcription job.

    Parameters
    ----------
    job_name : str
        Name of the transcription job.

    Returns
    -------
    dict
        Summary containing job status, transcript URL, duration, and speaker count.
    """
    client = get_speech_client("boto3")
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response["TranscriptionJob"]
    summary = {
        "job_name": job_name,
        "status": job["TranscriptionJobStatus"],
        "transcript_url": job["Transcript"]["TranscriptFileUri"],
        "duration_seconds": job["Media"]["MediaFileUri"]
        .split("/")[-1]
        .split(",")[0],  # placeholder, real logic needed
        "speaker_labels": job.get("Settings", {}).get(
            "EnableSpeakerIdentification", False
        ),
    }
    return summary
