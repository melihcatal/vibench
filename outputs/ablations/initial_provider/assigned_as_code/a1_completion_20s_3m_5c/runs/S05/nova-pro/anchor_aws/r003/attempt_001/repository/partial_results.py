import asyncio

from amazon_transcribe.model import TranscriptEvent

async def handle_partial_results(stream):
    async for event in stream.output_stream:
        if isinstance(event, TranscriptEvent):
            for result in event.transcript.results:
                if result.alternatives:
                    yield {'text': result.alternatives[0].transcript, 'is_final': not result.is_partial}