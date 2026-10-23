import os
import boto3
from speech_client import get_transcribe_client

def diarized_transcript(file_path, transcript_job_name):
    client = get_transcribe_client()
    response = client.start_transcription_job(
        TranscriptionJobName=transcript_job_name,
        Media={'MediaFileUri': f's3://{os.getenv("AWS_S3_BUCKET__BATCH_AUDIO")}/{file_path}"},
        MediaFormat='mp3',
        Settings={
            'LanguageCode': 'en-US',
            'EnableSpeakerDiarization': True,
            'MaxSpeakerLabels': 10,
        },
    )
    print(f"Diarized job submitted: {response['TranscriptionJob']['TranscriptionJobName']}")
    return response['TranscriptionJob']['TranscriptionJobName']