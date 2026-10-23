import os
from typing import Optional
from deepgram import DeepgramClient, DeepgramClientOptions


def load_deepgram_config() -> dict:
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")
    return {"api_key": api_key}


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    if api_key is None:
        config = load_deepgram_config()
        api_key = config["api_key"]
    options = DeepgramClientOptions(api_key=api_key)
    return DeepgramClient(options=options)


def get_streaming_options(
    language: str = "en",
    punctuation: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
    model: str = "nova-2",
    encoding: str = "linear16",
    sample_rate: int = 16000,
    channels: int = 1,
) -> dict:
    return {
        "model": model,
        "language": language,
        "punctuate": punctuation,
        "interim_results": interim_results,
        "smart_format": smart_format,
        "encoding": encoding,
        "sample_rate": sample_rate,
        "channels": channels,
    }
