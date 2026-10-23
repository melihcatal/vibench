import boto3

def transcribe_audio(audio_file_path):
    client = boto3.client('transcribe', region_name='us-west-2')
    job_name = 'qa_transcription_job'
    job_uri = f's3://my-qa-samples-bucket/{audio_file_path}'
    
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    
    # Wait for the transcription job to complete
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = client.get_object(Bucket='my-qa-samples-bucket', Key=transcript_uri.split('/')[-1])
        transcript = response['Body'].read().decode('utf-8')
        return transcript
    else:
        return 'Transcription failed'

if __name__ == '__main__'):
    audio_file = 'sample_qa.mp3'
    transcript = transcribe_audio(audio_file)
    print(transcript)