from speech_client import get_speech_client

async def start_stream_with_language(language_code="en-US", enable_punctuation=True):
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "config": {
                "encoding": "LINEAR16",
                "sample_rate_hertz": 16000,
                "language_code": language_code,
                "model": "latest_long",
                "enable_automatic_punctuation": enable_punctuation,
            },
            "single_utterance": False,
        }
    )
    return stream