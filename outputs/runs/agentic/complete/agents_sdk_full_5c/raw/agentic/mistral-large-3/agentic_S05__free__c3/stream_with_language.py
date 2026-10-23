from speech_client import get_speech_client

async def stream_with_language(language: str = "en", enable_punctuation: bool = True):
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "model": "whisper-1",
            "language": language,
            "response_format": "text",
            "punctuation": enable_punctuation,
        }
    )
    return stream