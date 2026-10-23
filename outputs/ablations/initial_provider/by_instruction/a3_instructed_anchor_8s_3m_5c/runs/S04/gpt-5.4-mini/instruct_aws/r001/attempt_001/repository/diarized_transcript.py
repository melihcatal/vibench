from speech_client import get_transcribe_client


def request_diarized_transcript(audio_uri: str, language_code: str = "en-US"):
    client = get_transcribe_client()
    return client.start_transcription_job(
        TranscriptionJobName=f"diarized-{audio_uri.rsplit('/', 1)[-1]}",
        Media={"MediaFileUri": audio_uri},
        MediaFormat="mp3",
        LanguageCode=language_code,
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
