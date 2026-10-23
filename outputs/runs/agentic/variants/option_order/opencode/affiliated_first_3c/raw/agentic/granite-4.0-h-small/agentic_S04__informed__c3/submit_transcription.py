# SAME-SCENARIO submit transcription using Amazon Transcribe
import boto3
import os

# Load configuration (environment variables are expected to be set)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# Create a Transcribe service client
client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def submit_transcription(job_name, audio_file_path):
    """Submit an audio file for batch transcription with speaker diarization.

    Args:
        job_name (str): Name of the Transcribe job.
        audio_file_path (str): Path to the audio file.

    Returns:
        str: The transcription job name.
    """
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file_path},
        MediaFormat="mp3",  # adjust based on your audio format
        LanguageCode="en-US",
        Settings={
            "VocabularyName": os.getenv("VOCABULARY_NAME", None),
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10,
        },
    )
    print(f"Transcription job submitted: {job_name}")
    return job_name


# Example usage (to be run as a script):
if __name__ == "__main__":
    job_name = "my-batch-job-" + os.getenv("RUN_ID", "1")
    audio_path = os.getenv("AUDIO_FILE_PATH")
    if audio_path:
        submit_transcription(job_name, audio_path)
