import os
from deepgram import DeepgramClient, DeepgramClientOptions


def load_api_key() -> str:
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is not set")
    return api_key


def create_deepgram_client(api_key: str | None = None) -> DeepgramClient:
    key = api_key or load_api_key()
    options = DeepgramClientOptions(options={"keepalive": "true"})
    return DeepgramClient(key, options)


def get_default_language() -> str:
    return os.environ.get("DEEPGRAM_DEFAULT_LANGUAGE", "en-US")


def get_default_model() -> str:
    return os.environ.get("DEEPGRAM_DEFAULT_MODEL", "nova-2")


def build_streaming_options(
    language: str | None = None,
    punctuate: bool = True,
    interim_results: bool = True,
    model: str | None = None,
    smart_format: bool = True,
) -> dict:
    opts: dict = {
        "model": model or get_default_model(),
        "punctuate": punctuate,
        "interim_results": interim_results,
        "smart_format": smart_format,
    }
    if language:
        opts["language"] = language
    return opts
