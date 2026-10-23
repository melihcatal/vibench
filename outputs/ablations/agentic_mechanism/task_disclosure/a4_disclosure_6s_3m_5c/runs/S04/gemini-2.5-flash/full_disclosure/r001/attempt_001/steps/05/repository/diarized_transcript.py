import boto3
import os

def request_diarization(audio_file_uri: str, job_name: str, language_code: str = "en-US"):
    """
    Requests speaker diarization for a recorded meeting using AWS Transcribe.

    Args:
        audio_file_uri (str): The S3 URI of the audio file (e.g., "s3://your-bucket/your-audio-file.flac").
        job_name (str): A unique name for the transcription job.
        language_code (str): The language code of the audio (e.g., "en-US").

    Returns:
        str: The name of the transcription job.
    """
    client = boto3.client("transcribe", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat="flac",  # Assuming FLAC for this example, adjust as needed
        Media={
            "MediaFileUri": audio_file_uri
        },
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10  # Adjust the maximum number of speakers as needed
        }
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]