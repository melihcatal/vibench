from __future__ import annotations

from typing import Any, AsyncIterator, Iterable, Optional

from google.cloud import speech_v1p1beta1 as speech


def build_streaming_config(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: str = "latest_long",
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
    )
    return speech.StreamingRecognitionConfig(config=config, interim_results=interim_results)


async def stream_with_language(
    audio_chunks: AsyncIterator[bytes],
    *,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
    model: str = "latest_long",
    client: Optional[Any] = None,
) -> AsyncIterator[dict[str, object]]:
    speech_client = client or speech.SpeechClient()
    streaming_config = build_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        interim_results=interim_results,
    )

    def request_iter() -> Iterable[speech.StreamingRecognizeRequest]:
        async def _generator() -> AsyncIterator[speech.StreamingRecognizeRequest]:
            async for chunk in audio_chunks:
                if chunk:
                    yield speech.StreamingRecognizeRequest(audio_content=chunk)

        return _generator()

    responses = speech_client.streaming_recognize(streaming_config, request_iter())
    for response in responses:
        for result in getattr(response, "results", []) or []:
            if not getattr(result, "alternatives", None):
                continue
            transcript = getattr(result.alternatives[0], "transcript", "") or ""
            if not transcript:
                continue
            yield {"transcript": transcript, "final": bool(getattr(result, "is_final", False))}
