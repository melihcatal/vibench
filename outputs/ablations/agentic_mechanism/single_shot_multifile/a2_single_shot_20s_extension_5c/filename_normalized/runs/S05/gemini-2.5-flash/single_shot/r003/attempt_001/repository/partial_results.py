import asyncio
import os
from typing import AsyncIterator

from google.cloud.speech_v1p1beta1.types import StreamingRecognizeResponse
from speech_models import TranscriptResult

async def process_streaming_recognition_responses(responses: AsyncIterator[StreamingRecognizeResponse]) -> AsyncIterator[TranscriptResult]:
    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        alternative = result.alternatives[0]

        is_final = result.is_final
        transcript = alternative.transcript
        confidence = alternative.confidence if is_final else 0.0

        if transcript:
            yield TranscriptResult(
                transcript=transcript,
                confidence=confidence,
                is_final=is_final,
                language_code=result.language_code
            )
