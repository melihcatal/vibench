import asyncio
from typing import AsyncGenerator
from speech_client import get_stt_client
from speech_models import StreamingConfig, create_live_options
from deepgram import LiveTranscriptionEvents

class PartialResultsHandler:
    def __init__(self):
        self.buffer = ""
        self.partial = ""

    def on_transcript(self, result):
        transcript = result.channel.alternatives[0].transcript.strip()
        if result.speech_final:
            self.buffer += transcript + " "
            print(f"FINAL: {transcript}")
            self.partial = ""
            return "final", transcript
        else:
            self.partial = transcript
            print(f"PARTIAL: {transcript}")
            return "interim", transcript

async def handle_streaming_events(stream_gen) -> AsyncGenerator[tuple[str, str], None]:
    handler = PartialResultsHandler()
    async for typ, text in stream_gen:
        yield handler.on_transcript  # adapt
        # Note: integrate as event handler
