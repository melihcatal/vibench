# SAME-SCENARIO fetch word/segment timestamps from a completed transcription job using Amazon Transcribe
import boto3
import os

# Load AWS credentials and region from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def get_timestamped_transcript(job_name):
    """Retrieve the timestamped transcript for a completed job.

    Args:
        job_name (str): The Transcribe job name returned from submission.

    Returns:
        list: List of timestamped words/segments.
    """
    result = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript = result["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    # In this example we simply return the URL; downstream code can download and parse the
    # transcript JSON to extract timestamps.
    print(f"Timestamped transcript available at: {transcript}")
    return transcript


# CLI entry point
if __name__ == "__main__":
    job = os.getenv("JOB_NAME")  # passed from previous step
    if job:
        get_timestamped_transcript(job)
