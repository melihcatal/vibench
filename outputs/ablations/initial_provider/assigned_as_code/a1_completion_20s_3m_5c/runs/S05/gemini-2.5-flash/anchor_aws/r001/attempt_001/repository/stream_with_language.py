import asyncio
from typing import AsyncIterable

from speech_client import AWSStreamClient
from speech_models import TranscriptSegment, StreamingRecognitionConfig


async def stream_with_language(audio_chunks: AsyncIterable[bytes], language_code: str, sample_rate_hz: int, enable_automatic_punctuation: bool = True):
    # Note: AWS Transcribe handles punctuation automatically based on language code.
    # The 'enable_automatic_punctuation' parameter here is more for conceptual alignment
    # with other STT providers that might have an explicit setting.
    # AWS Transcribe doesn't have a direct 'enable_automatic_punctuation' flag in its StartStreamTranscription API.
    # Punctuation is generally included by default for supported languages.

    config = StreamingRecognitionConfig(
        language_code=language_code,
        sample_rate_hz=sample_rate_hz,
    )

    client = AWSStreamClient(region="us-east-1")
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
