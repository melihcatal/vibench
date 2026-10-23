from speech_client import get_openai_client, get_transcription_model, open_audio


def submit_transcription(audio_path, language=None):
    client = get_openai_client()
    with open_audio(audio_path) as audio:
        kwargs = {"model": get_transcription_model(), "file": audio}
        if language:
            kwargs["language"] = language
        return client.audio.transcriptions.create(**kwargs)
