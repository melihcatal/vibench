import os
import boto3

transcribe = boto3.client('transcribe')

def transcribe_audio(file_uri):
    job_name = 'tts_qa_transcript_job'
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        return status['TranscriptionJob']['Transcripts'][0]['TranscriptFileUri']
    else:
        return None
