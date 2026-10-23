import speech_client

def submit_diarized_transcription_job(audio_s3_uri: str, job_name: str, language_code: str = "en-US", max_speakers: int = 2) -> dict:
    transcribe_client = speech_client.get_transcribe_client()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_s3_uri},
        MediaFormat='mp3',
        LanguageCode=language_code,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': max_speakers,
        }
    )
    return response['TranscriptionJob']