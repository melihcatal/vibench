import os
from typing import Optional
from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents
from deepgram.clients.live.v1 import LiveOptions


def get_deepgram_api_key() -> str:
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is not set")
    return api_key


def create_deepgram_client(api_key: Optional[str] = None) -> DeepgramClient:
    key = api_key or get_deepgram_api_key()
    options = DeepgramClientOptions(options={"keepalive": "true"})
    return DeepgramClient(key, options)


def build_live_options(
    model: str = "nova-2",
    language: str = "en-US",
    encoding: str = "linear16",
    sample_rate: int = 16000,
    channels: int = 1,
    interim_results: bool = True,
    punctuate: bool = True,
    smart_format: bool = True,
    profanity_filter: bool = False,
    diarize: bool = False,
    vad_events: bool = True,
    extra: Optional[dict] = None,
) -> LiveOptions:
    opts = {
        "model": model,
        "language": language,
        "encoding": encoding,
        "sample_rate": sample_rate,
        "channels": channels,
        "interim_results": interim_results,
        "punctuate": punctuate,
        "smart_format": smart_format,
        "profanity_filter": profanity_filter,
        "diarize": diarize,
        "vad_events": vad_events,
    }
    if extra:
        opts.update(extra)
    return LiveOptions(**opts)


def register_default_handlers(
    dg_connection,
    on_interim=None,
    on_final=None,
    on_error=None,
    on_open=None,
    on_close=None,
    on_metadata=None,
    on_utterance_end=None,
    on_speech_started=None,
    on_speech_ended=None,
):
    if on_open:
        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    if on_interim:
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_interim)
    if on_final:
        dg_connection.on(LiveTranscriptionEvents.FinalTranscript, on_final)
    if on_error:
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
    if on_close:
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    if on_metadata:
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
    if on_utterance_end:
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
    if on_speech_started:
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
    if on_speech_ended:
        dg_connection.on(LiveTranscriptionEvents.SpeechEnded, on_speech_ended)
