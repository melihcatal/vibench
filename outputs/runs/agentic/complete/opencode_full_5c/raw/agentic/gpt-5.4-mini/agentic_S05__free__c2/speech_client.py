import os
from dataclasses import asdict
from typing import Any, AsyncIterable, Dict, Iterable, List

from google.cloud import speech

from speech_models import SpeechStreamConfig, normalize_chunks


def load_stream_config() -> SpeechStreamConfig:
    return SpeechStreamConfig(
        language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US"),
        enable_automatic_punctuation=os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "1")
        != "0",
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
    )


def build_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_streaming_config(
    config: SpeechStreamConfig,
) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE", "16000")),
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
        model=config.model,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )


def chunk_bytes(chunks: Iterable[bytes]) -> List[speech.StreamingRecognizeRequest]:
    return [
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in chunks
        if chunk
    ]


async def async_chunk_requests(
    source: AsyncIterable[bytes],
) -> AsyncIterable[speech.StreamingRecognizeRequest]:
    async for chunk in source:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)


def config_as_dict(config: SpeechStreamConfig) -> Dict[str, Any]:
    return asdict(config)
