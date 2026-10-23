from speech_client import build_client, get_openai_audio_model


def diarized_transcript(file_path: str, language: str = None):
    client = build_client()
    with open(file_path, "rb") as audio:
        kwargs = {
            "model": get_openai_audio_model(),
            "file": audio,
            "response_format": "verbose_json",
            "timestamp_granularities": ["segment"],
        }
        if language:
            kwargs["language"] = language
        return client.audio.transcriptions.create(**kwargs)
