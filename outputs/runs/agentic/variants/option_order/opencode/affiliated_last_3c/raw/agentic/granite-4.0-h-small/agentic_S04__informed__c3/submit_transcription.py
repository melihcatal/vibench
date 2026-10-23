import os
import boto3
from speech_client import SpeechClient

# Configure AWS credentials via environment variables or config file
client = SpeechClient()  # uses boto3 under the hood


def submit_transcription(audio_file_path, job_name):
    """Submits an audio file for batch transcription using Amazon Transcribe.
    Returns the job ID for later polling.
    """
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    # Use the helper client to build the request payload
    payload = client.create_batch_transcription_payload(audio_file_path, job_name)
    response = client.transcribe.start_transcription_job(**payload)
    return response["TranscriptionJob"]["TranscriptionJobName"]
