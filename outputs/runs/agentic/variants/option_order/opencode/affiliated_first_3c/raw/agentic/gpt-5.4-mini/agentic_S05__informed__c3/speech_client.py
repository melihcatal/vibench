import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable, Iterable, Iterator, Optional

from deepgram import DeepgramClient, LiveTranscriptionEvents


@dataclass
class SpeechClientConfig:
    api_key: str
    model: str = "nova-2"
    language: Optional[str] = None
    punctuate: bool = True
    interim_results: bool = True


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
        language=os.getenv("DEEPGRAM_LANGUAGE"),
        punctuate=os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() == "true",
        interim_results=os.getenv("DEEPGRAM_INTERIM_RESULTS", "true").lower() == "true",
    )


def build_deepgram_client(
    config: Optional[SpeechClientConfig] = None,
) -> DeepgramClient:
    return DeepgramClient(config.api_key if config else load_speech_config().api_key)


def deepgram_live_options(
    config: Optional[SpeechClientConfig] = None,
) -> dict[str, Any]:
    cfg = config or load_speech_config()
    options: dict[str, Any] = {
        "model": cfg.model,
        "punctuate": cfg.punctuate,
        "interim_results": cfg.interim_results,
        "smart_format": True,
    }
    if cfg.language:
        options["language"] = cfg.language
    return options


def attach_transcript_handler(
    connection: Any, callback: Callable[[str, bool], None]
) -> None:
    def _on_message(_: Any, result: Any, **__: Any) -> None:
        channel = getattr(result, "channel", None)
        alternatives = getattr(channel, "alternatives", None) if channel else None
        transcript = getattr(alternatives[0], "transcript", "") if alternatives else ""
        is_final = bool(getattr(result, "is_final", False))
        if transcript:
            callback(transcript, is_final)

    connection.on(LiveTranscriptionEvents.Transcript, _on_message)


async def iterate_audio_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    async for chunk in source:
        yield chunk


def iter_audio_chunks(source: Iterable[bytes]) -> Iterator[bytes]:
    yield from source
