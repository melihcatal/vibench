import os
import boto3

time
from speech_client import get_speech_client


def poll_transcription(job_name, max_attempts=10, wait_seconds=5):
    """Poll an ongoing transcription job until it completes and return the transcript URL.

    Parameters
    ----------
    job_name : str
        The name of the transcription job to poll.
    max_attempts : int, optional
        Maximum number of poll attempts (default 10).
    wait_seconds : int, optional
        Seconds to wait between attempts (default 5).

    Returns
    -------
    str
        S3 URI of the completed transcript file.
    """
    client = get_speech_client("boto3")
    attempts = 0
    while attempts < max_attempts:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        elif status == "FAILED":
            raise RuntimeError("Transcription job failed")
        time.sleep(wait_seconds)
        attempts += 1
    raise TimeoutError("Transcription job did not complete within timeout")
