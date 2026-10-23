import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_result

async def stream_chunks(audio_source):
    client = get_speech_client()
    config = {
        "config": {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 16000,
            "language_code": "en-US",
            "model": "latest_long",
            "enable_automatic_punctuation": True,
        },
        "single_utterance": False,
    }

    stream = client.streaming_recognize(config, handle_partial_result)

    try:
        async for chunk in audio_source:
            await stream.send(chunk)
    except asyncio.CancelledError:
        await stream.close()