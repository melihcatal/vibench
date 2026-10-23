from speech_client import build_client, get_openai_audio_model


def timestamped_transcript(file_path: str, granularity: str = "word"):
    client = build_client()
    with open(file_path, "rb") as audio:
        return client.audio.transcriptions.create(
            model=get_openai_audio_model(),
            file=audio,
            response_format="verbose_json",
            timestamp_granularities=[granularity],
        )
