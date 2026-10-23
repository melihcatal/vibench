import boto3

transcribe_client = boto3.client('transcribe')

def transcribe_audio(audio_file_path):
    job_name = 'qa_transcription_job'
    job_uri = 's3://your-bucket/' + audio_file_path
    
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket='your-bucket', Key=transcript_uri.split('/')[-1])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription failed'

# Example usage
audio_file_path = 'path/to/your/audio/file.mp3'
transcript = transcribe_audio(audio_file_path)
print(transcript)