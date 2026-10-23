import boto3

def transcribe_audio(audio_file):
    transcribe_client = boto3.client('transcribe')
    job_name = 'tts_qa_transcription'
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    # Wait for the job to complete and return the transcript
    # This is a simplified example; in practice, you should handle job status and results
    return 'Transcription job started'