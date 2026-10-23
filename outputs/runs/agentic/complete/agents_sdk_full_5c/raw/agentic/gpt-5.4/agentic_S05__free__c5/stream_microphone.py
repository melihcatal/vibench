import asyncio
from typing import AsyncIterator, Iterable, Optional

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import get_recognizer_path, get_speech_client
from speech_models import TranscriptChunk, normalize_transcript_text


async def stream_microphone(
    audio_source: AsyncIterator[bytes],
    sample_rate_hz: int = 16000,
    language_code: str = "en-US",
    recognizer: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    client = get_speech_client()
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model="latest_short",
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            interim_results=True
        ),
    )

    async def request_iter() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=get_recognizer_path(recognizer=recognizer),
            streaming_config=streaming_config,
        )
        async for chunk in audio_source:
            if chunk:
                yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = await client.streaming_recognize(requests=request_iter())
    async for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            alt = result.alternatives[0]
            yield TranscriptChunk(
                text=normalize_transcript_text(alt.transcript),
                is_final=result.is_final,
                stability=getattr(result, "stability", None),
                language_code=language_code,
            )
