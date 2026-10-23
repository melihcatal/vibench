from speech_client import get_transcribe_client


def diarized_transcript(
    audio_uri: str, job_name: str = None, language_code: str = "en-US"
):
    client = get_transcribe_client()
    return client.start_transcription_job(
        TranscriptionJobName=job_name or "diarized-meeting",
        Media={"MediaFileUri": audio_uri},
        MediaFormat=audio_uri.rsplit(".", 1)[-1].lower(),
        LanguageCode=language_code,
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
