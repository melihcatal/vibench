import speech_client

def submit_transcription_job(audio_s3_uri: str, job_name: str, language_code: str = "en-US") -> dict:
    transcribe_client = speech_client.get_transcribe_client()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_s3_uri},
        MediaFormat='mp3',
        LanguageCode=language_code,
    )
    return response['TranscriptionJob']