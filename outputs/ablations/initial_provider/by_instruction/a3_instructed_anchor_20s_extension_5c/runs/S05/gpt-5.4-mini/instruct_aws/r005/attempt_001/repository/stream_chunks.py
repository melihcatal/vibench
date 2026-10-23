from typing import AsyncIterator, Iterator

from speech_client import create_transcribe_streaming_client, load_speech_config
from speech_models import AudioChunk, normalize_transcript_event


async def stream_chunks(source: AsyncIterator[AudioChunk]) -> Iterator[str]:
    config = load_speech_config()
    client = create_transcribe_streaming_client(config.region_name)
    audio_stream = (chunk.data async for chunk in source)
    response = client.start_stream_transcription(
        language_code=config.language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
        audio_stream=audio_stream,
    )
    for event in response["TranscriptResultStream"]:
        normalized = normalize_transcript_event(event)
        if normalized.text:
            yield normalized.text
