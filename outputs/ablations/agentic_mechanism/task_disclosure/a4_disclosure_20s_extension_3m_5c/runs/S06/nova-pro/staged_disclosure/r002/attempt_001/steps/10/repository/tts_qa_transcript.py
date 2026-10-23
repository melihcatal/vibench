import boto3

def transcribe_audio(file_path):
    transcribe = boto3.client('transcribe', region_name='us-west-2')
    job_name = 'qa_transcription_job'
    job_uri = f's3://my-qa-samples-bucket/{file_path}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    # Wait for the transcription job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = boto3.client('s3').get_object(Bucket='my-qa-samples-bucket', Key=transcript_uri.split('/')[-1])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription failed'

# Example usage
transcript = transcribe_audio('example.mp3')
print(transcript)