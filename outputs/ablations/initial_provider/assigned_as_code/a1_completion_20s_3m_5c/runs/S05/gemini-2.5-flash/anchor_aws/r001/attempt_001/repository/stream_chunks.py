import asyncio
from typing import AsyncIterable

from speech_client import AWSStreamClient
from speech_models import TranscriptSegment, StreamingRecognitionConfig


async def stream_chunks(audio_chunks: AsyncIterable[bytes], config: StreamingRecognitionConfig):
    client = AWSStreamClient(region="us-east-1") # Using a fixed region for this example, could be configured
    stream = await client.start_transcription_stream(
        language_code=config.language_code, sample_rate_hz=config.sample_rate_hz
    )

    sender = asyncio.create_task(client.generate_audio_events(audio_chunks, stream.input_stream))

    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield TranscriptSegment(
                        text=result.alternatives[0].transcript,
                        is_final=not result.is_partial,
                        start_time=result.start_time,
                        end_time=result.end_time,
                        alternatives=[
                            {
                                "transcript": alt.transcript,
                                "confidence": alt.confidence,
                            }
                            for alt in result.alternatives
                        ],
                    )
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
