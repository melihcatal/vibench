from typing import AsyncIterator, Iterator

from speech_client import load_speech_config, make_transcribe_streaming_client
from speech_models import TranscriptChunk


async def stream_audio_chunks(source: AsyncIterator[bytes]) -> Iterator[TranscriptChunk]:
    config = load_speech_config()
    client = make_transcribe_streaming_client(config.region_name)
    def audio_events():
        async def _aiter():
            async for chunk in source:
                yield {"AudioEvent": {"AudioChunk": chunk}}
        return _aiter()
    response = client.start_stream_transcription(
        LanguageCode=config.language_code,
        MediaSampleRateHertz=config.media_sample_rate_hz,
        MediaEncoding=config.media_encoding,
        AudioStream=audio_events(),
    )
    for event in response["TranscriptResultStream"]:
        for result in event.get("TranscriptEvent", {}).get("Transcript", {}).get("Results", []):
            alternatives = result.get("Alternatives", [])
            if alternatives:
                yield TranscriptChunk(text=alternatives[0].get("Transcript", ""), is_partial=result.get("IsPartial", False), language_code=config.language_code)
