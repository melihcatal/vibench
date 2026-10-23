import os
from deepgram import DeepgramClient, LiveOptions
from speech_models import STTConfig


def get_stt_client() -> DeepgramClient:
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required.")
    return DeepgramClient(api_key)


def get_live_options(config: STTConfig | None = None) -> LiveOptions:
    if config is None:
        config = STTConfig()
    return LiveOptions(
        punctuate=config.punctuate,
        interim_results=config.interim_results,
        language=config.language,
        model=config.model,
        smart_format=True,
    )
