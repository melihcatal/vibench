import asyncio
from typing import AsyncIterator, List, Optional

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    load_config,
    build_recognizer_path,
    build_streaming_config,
    validate_config,
)
from speech_models import (
    StreamingRecognitionRequest,
    StreamingRecognitionResult,
    WordInfo,
)


class AudioChunkSource:
    def __init__(self, chunks: List[bytes], chunk_delay: float = 0.1):
        self.chunks = chunks
        self.chunk_delay = chunk_delay
        self._index = 0

    async def __aiter__(self):
        for chunk in self.chunks:
            await asyncio.sleep(self.chunk_delay)
            yield chunk
        self._index = len(self.chunks)

    def is_exhausted(self) -> bool:
        return self._index >= len(self.chunks)


async def stream_chunks(
    audio_source: AsyncIterator[bytes],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_punctuation: bool = True,
) -> AsyncIterator[StreamingRecognitionResult]:
    config = load_config()
    validate_config(config)
    config.language_code = language_code
    config.sample_rate_hertz = sample_rate_hertz
    config.enable_automatic_punctuation = enable_punctuation

    client = speech_v2.SpeechClient()
    recognizer = build_recognizer_path(config)

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[language_code],
            model=config.model,
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=enable_punctuation,
                enable_word_time_offsets=config.enable_word_time_offsets,
            ),
        ),
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for audio_chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=audio_chunk)
        yield cloud_speech.StreamingRecognizeRequest(audio=b"")

    responses = client.streaming_recognize(
        recognizer=recognizer,
        requests=request_generator(),
    )

    for response in responses:
        for result in response.results:
            words = [
                WordInfo(
                    word=w.word,
                    start_offset_seconds=w.start_offset.seconds
                    + w.start_offset.microseconds / 1_000_000,
                    end_offset_seconds=w.end_offset.seconds
                    + w.end_offset.microseconds / 1_000_000,
                    confidence=w.confidence,
                )
                for w in result.word_info
            ]
            yield StreamingRecognitionResult(
                transcript=result.alternatives[0].transcript,
                is_final=result.is_final,
                stability=result.stability,
                confidence=result.alternatives[0].confidence,
                words=words,
                language_code=language_code,
            )
