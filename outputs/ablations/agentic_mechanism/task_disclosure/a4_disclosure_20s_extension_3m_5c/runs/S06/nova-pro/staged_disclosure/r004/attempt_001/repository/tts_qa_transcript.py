import boto3

transcribe_client = boto3.client('transcribe')

def transcribe_audio(audio_file_path):
    job_name = 'qa_transcription_job'
    job_uri = f's3://your-bucket-name/{audio_file_path}'

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    while True:
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break

    if job_status == 'COMPLETED':
        transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript = boto3.client('s3').get_object(Bucket='your-bucket-name', Key=transcript_uri.split('/')[-1])['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription failed'

# Example usage
audio_file_path = 'path/to/your/audio/file.mp3'
transcript = transcribe_audio(audio_file_path)
print(transcript)