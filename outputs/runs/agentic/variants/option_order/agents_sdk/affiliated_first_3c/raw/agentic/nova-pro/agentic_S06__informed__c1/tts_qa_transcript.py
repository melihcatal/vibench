import os
import boto3

transcribe_client = boto3.client('transcribe', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def transcribe_audio(file_path):
    job_name = 'tts_qa_transcript'
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_path},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    return response['TranscriptionJob']['Transcript']['TranscriptFileUri']