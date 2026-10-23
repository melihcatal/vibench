import os
import boto3

def transcribe_audio(audio_data):
    transcribe = boto3.client('transcribe', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    with open('audio.mp3', 'wb') as file:
        file.write(audio_data)
    job_name = 'tts_qa_transcript'
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': 's3://my-bucket/audio.mp3'},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = requests.get(transcript_uri)
        return response.text
    else:
        return 'Transcription failed'