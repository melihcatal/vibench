import boto3

def transcribe_audio(audio_file_path):
    transcribe = boto3.client('transcribe')
    job_name = 'qa_transcription_job'
    job_uri = f's3://your-bucket-name/{audio_file_path}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f'Transcription completed. Transcript URI: {transcript_uri}')
    else:
        print('Transcription failed.')

# Example usage:
# transcribe_audio('path/to/audio/file.mp3')