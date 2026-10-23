import boto3

def transcribe_audio(audio_file_path):
    transcribe = boto3.client('transcribe', region_name='us-west-2')
    job_name = 'tts_qa_transcription_job'
    job_uri = 's3://my-qa-audio-bucket/' + audio_file_path
    
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
        transcript_uri = status['TranscriptionJob']['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_content = boto3.client('s3').get_object(Bucket='my-qa-transcripts-bucket', Key=transcript_uri.split('/')[-1])['Body'].read().decode('utf-8')
        return transcript_content
    else:
        return 'Transcription failed'

# Example usage:
# audio_file_path = 'path/to/synthesized_audio.mp3'
# print(transcribe_audio(audio_file_path))