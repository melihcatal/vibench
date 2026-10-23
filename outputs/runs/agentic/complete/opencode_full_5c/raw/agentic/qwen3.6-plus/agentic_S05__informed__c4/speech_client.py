import os
from typing import Optional
from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents
from deepgram.clients.live.v1 import LiveOptions


def load_deepgram_config(api_key: Optional[str] = None) -> dict:
    key = api_key or os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")
    return {"api_key": key}


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    config = load_deepgram_config(api_key)
    options = DeepgramClientOptions(api_key=config["api_key"])
    return DeepgramClient(config=config["api_key"])


def build_live_options(
    model: str = "nova-2",
    language: str = "en",
    punctuate: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
    encoding: str = "linear16",
    sample_rate: int = 16000,
    channels: int = 1,
) -> LiveOptions:
    return LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        smart_format=smart_format,
        encoding=encoding,
        sample_rate=sample_rate,
        channels=channels,
    )


def register_transcript_handlers(
    connection,
    on_interim=None,
    on_final=None,
    on_error=None,
    on_open=None,
    on_close=None,
):
    if on_interim:
        connection.on(LiveTranscriptionEvents.Transcript, on_interim)
    if on_final:
        connection.on(LiveTranscriptionEvents.Transcript, on_final)
    if on_error:
        connection.on(LiveTranscriptionEvents.Error, on_error)
    if on_open:
        connection.on(LiveTranscriptionEvents.Open, on_open)
    if on_close:
        connection.on(LiveTranscriptionEvents.Close, on_close)
