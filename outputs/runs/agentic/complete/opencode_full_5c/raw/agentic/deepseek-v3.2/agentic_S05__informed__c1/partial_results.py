import asyncio
from typing import Dict, Any, Optional
from deepgram import Deepgram
import os


class StreamingRecognitionHandler:
    def __init__(self):
        self.dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
        self.connection = None
        self.partial_buffer = ""
        self.final_results = []

    async def start_stream(self, options: Optional[Dict[str, Any]] = None):
        if options is None:
            options = {}

        default_options = {
            "model": "nova-2",
            "interim_results": True,
            "smart_format": True,
            "encoding": "linear16",
            "sample_rate": 16000,
            "channels": 1,
        }
        default_options.update(options)

        self.connection = await self.dg_client.transcription.live(default_options)
        return self.connection

    async def process_audio_chunk(self, audio_chunk: bytes):
        if self.connection:
            await self.connection.send(audio_chunk)

    async def receive_events(self):
        if not self.connection:
            raise RuntimeError("Stream not started")

        async for event in self.connection:
            yield await self._handle_event(event)

    async def _handle_event(self, event: Dict[str, Any]):
        event_type = "unknown"
        transcript = ""
        is_final = False

        if "type" in event and event["type"] == "Results":
            if "channel" in event:
                alternatives = event["channel"].get("alternatives", [])
                if alternatives and "transcript" in alternatives[0]:
                    transcript = alternatives[0]["transcript"]
                    is_final = event.get("is_final", False)

                    if is_final:
                        event_type = "final_transcript"
                        self.final_results.append(transcript)
                        self.partial_buffer = ""
                    else:
                        event_type = "partial_transcript"
                        self.partial_buffer = transcript
            elif "speech_final" in event:
                event_type = "speech_final"
        elif "type" in event and event["type"] == "Metadata":
            event_type = "metadata"
        elif "type" in event and event["type"] == "Error":
            event_type = "error"

        return {
            "type": event_type,
            "transcript": transcript,
            "is_final": is_final,
            "partial_buffer": self.partial_buffer,
            "final_results": self.final_results.copy(),
        }

    async def close(self):
        if self.connection:
            await self.connection.finish()


async def example_handler():
    handler = StreamingRecognitionHandler()

    await handler.start_stream()

    test_chunks = [b"\x00" * 1024 for _ in range(5)]

    for chunk in test_chunks:
        await handler.process_audio_chunk(chunk)
        await asyncio.sleep(0.1)

        try:
            async for event in handler.receive_events():
                if event["type"] in ["partial_transcript", "final_transcript"]:
                    prefix = (
                        "PARTIAL" if event["type"] == "partial_transcript" else "FINAL"
                    )
                    print(f"{prefix}: {event['transcript']}")
        except:
            pass

    await handler.close()


if __name__ == "__main__":
    asyncio.run(example_handler())
