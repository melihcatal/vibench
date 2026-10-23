# SAME-SCENARIO request speaker diarization in transcription job using Amazon Transcribe
import boto3
import os

# Configuration from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def diarized_transcription(job_name, audio_file_path):
    """Submit a transcription job that includes speaker diarization.

    Args:
        job_name (str): Desired job identifier.
        audio_file_path (str): Path to the audio file to transcribe.

    Returns:
        str: Job name (useful for later polling).
    """
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file_path},
        MediaFormat="mp3",  # adjust to match your file (mp3, wav, etc.)
        LanguageCode="en-US",
        Settings={
            "VocabularyName": os.getenv("VOCABULARY_NAME", None),
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10,  # max number of speakers to detect
        },
    )
    print(f"Diarized transcription job submitted: {job_name}")
    return job_name


# Example entry point for CLI use
if __name__ == "__main__":
    job_name = "diarized-batch-" + os.getenv("RUN_ID", "1")
    audio_path = os.getenv("AUDIO_FILE_PATH")
    if audio_path:
        diarized_transcription(job_name, audio_path)
