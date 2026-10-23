from typing import AsyncIterator, Optional

from speech_client import load_config, stream_transcript_events
from speech_models import SpeechRequest, TranscriptChunk


async def stream_with_language(audio_chunks: AsyncIterator[bytes], language: Optional[str] = "en-US") -> AsyncIterator[TranscriptChunk]:
    config = load_config(language=language, enable_punctuation=True)
    request = SpeechRequest(language=config.language, enable_punctuation=True, model=config.model)
    async for item in stream_transcript_events(audio_chunks, request=request):
        yield item
