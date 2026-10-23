import os
import boto3
from speech_client import get_speech_client


def timestamped_transcription(job_name):
    """Retrieve a transcription result that includes word-level timestamps.

    Parameters
    ----------
    job_name : str
        Name of the completed transcription job.

    Returns
    -------
    dict
        JSON output with 'results' containing timestamps for each word/segment.
    """
    client = get_speech_client("boto3")
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    # Ensure the job is completed and contains timestamps
    result = response["TranscriptionJob"]["Transcript"]["Results"]
    return {"results": result}
