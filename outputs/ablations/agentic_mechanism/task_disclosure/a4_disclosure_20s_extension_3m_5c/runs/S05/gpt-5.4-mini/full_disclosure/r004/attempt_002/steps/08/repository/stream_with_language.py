from __future__ import annotations

import os
from typing import Any, AsyncIterator, Awaitable, Callable, Dict, Optional

import google.cloud.speech_v1 as speech


def _language_code(value: Optional[str]) -> str:
    return value or os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US")


def _enable_punctuation(value: Optional[bool]) -> bool:
    if value is not None:
        return value
    return os.getenv("GOOGLE_CLOUD_SPEECH_ENABLE_AUTOMATIC_PUNCTUATION", "true").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def build_streaming_config(
    language_code: Optional[str] = None,
    enable_automatic_punctuation: Optional[bool] = None,
    model: Optional[str] = None,
) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=int(os.getenv("GOOGLE_CLOUD_SPEECH_SAMPLE_RATE_HERTZ", "16000")),
        language_code=_language_code(language_code),
        enable_automatic_punctuation=_enable_punctuation(enable_automatic_punctuation),
        model=model or os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )


class StreamingSpeechRecognizer:
    def __init__(self, client: Optional[speech.SpeechClient] = None) -> None:
        self.client = client or speech.SpeechClient()

    async def recognize(
        self,
        audio_chunks: AsyncIterator[bytes],
        language_code: Optional[str] = None,
        enable_automatic_punctuation: Optional[bool] = None,
        model: Optional[str] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        config = build_streaming_config(language_code, enable_automatic_punctuation, model)

        async def request_stream() -> AsyncIterator[speech.StreamingRecognizeRequest]:
            yield speech.StreamingRecognizeRequest(streaming_config=config)
            async for chunk in audio_chunks:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        responses = self.client.streaming_recognize(requests=request_stream())
        for response in responses:
            for result in response.results:
                if not result.alternatives:
                    continue
                alternative = result.alternatives[0]
                yield {
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence,
                    "is_final": result.is_final,
                    "language_code": _language_code(language_code),
                    "punctuated": _enable_punctuation(enable_automatic_punctuation),
                }


def create_streaming_recognizer(
    client: Optional[speech.SpeechClient] = None,
) -> StreamingSpeechRecognizer:
    return StreamingSpeechRecognizer(client=client)
