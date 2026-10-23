import boto3

transcribe_client = boto3.client('transcribe')

def transcribe_audio(file_path):
    job_name = 'tts_qa_transcription_job'
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_path},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    # Wait for the job to complete and return the transcript
    # This is a placeholder for actual job polling and retrieval logic
    return 'Transcription completed'