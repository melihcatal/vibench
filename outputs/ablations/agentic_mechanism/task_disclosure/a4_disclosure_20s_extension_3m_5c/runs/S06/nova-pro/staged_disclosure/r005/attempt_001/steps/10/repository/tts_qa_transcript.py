import boto3

def transcribe_audio(audio_file_path):
    transcribe = boto3.client('transcribe')
    job_name = 'qa_transcription_job'
    job_uri = 's3://your-bucket/' + audio_file_path
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    
    # Additional code to check job status and retrieve results
    
    print('Transcription job started')

# Example usage:
# transcribe_audio('path/to/audio/file.mp3')