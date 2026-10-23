from typing import AsyncIterator

from speech_client import build_transcribe_stream_client, load_streaming_speech_config
from speech_models import normalize_result_payload


async def stream_audio_chunks(chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
    config = load_streaming_speech_config()
    client = build_transcribe_stream_client(config.region)
    stream = await client.start_stream_transcription(
        language_code=config.language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
    )
    async for audio_chunk in chunks:
        await stream.input_stream.send_audio_event(audio_chunk=audio_chunk)
        async for event in stream.output_stream:
            for result in event.get("Transcript", {}).get("Results", []):
                normalized = normalize_result_payload(result)
                if normalized.text:
                    yield normalized.text
