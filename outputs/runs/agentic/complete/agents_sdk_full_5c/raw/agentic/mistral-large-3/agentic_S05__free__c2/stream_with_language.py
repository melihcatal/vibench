from speech_client import get_speech_client
from partial_results import handle_partial_result

async def stream_with_language(language_code="en-US", enable_punctuation=True):
    client = get_speech_client()
    config = {
        "config": {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 16000,
            "language_code": language_code,
            "model": "latest_long",
            "enable_automatic_punctuation": enable_punctuation,
        },
        "single_utterance": False,
    }

    stream = client.streaming_recognize(config, handle_partial_result)
    return stream