import asyncio
from typing import AsyncGenerator
from speech_client import get_stt_client
from speech_models import StreamingConfig, create_live_options
from deepgram import LiveTranscriptionEvents
from stream_microphone import stream_microphone  # or stream_chunks

async def start_streaming_recognizer(language: str = "en", punctuate: bool = True, use_mic: bool = True) -> AsyncGenerator[tuple[str, str], None]:
    config = StreamingConfig(
        language=language,
        punctuate=punctuate,
    )
    if use_mic:
        async for typ, text in stream_microphone(config):
            yield typ, text
    else:
        # assume chunks from elsewhere
        pass  # integrate stream_chunks similarly
