import os
from deepgram import DeepgramClient
from deepgram.options import LiveOptions


def get_deepgram_client():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return DeepgramClient(api_key)


def get_live_options(language: str = "en-US", enable_punctuate: bool = True):
    options = LiveOptions(
        model="nova-2",
        language=language,
        punctuate=enable_punctuate,
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        interim_results=True,
        utterance_end_ms="1000",
        vad_events=True,
    )
    return options
