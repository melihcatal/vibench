import os
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()


class PartialResultsHandler:
    def __init__(self):
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        if not DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
        self.deepgram = Deepgram(DEEPGRAM_API_KEY)
        self.dg_connection = None

    def _handle_transcript_received(self, result):
        if result.is_final:
            print(f"Final Transcript: {result.channel.alternatives[0].transcript}")
        else:
            print(f"Partial Transcript: {result.channel.alternatives[0].transcript}")

    def _handle_error(self, error):
        print(f"Deepgram Error: {error}")

    async def start_recognition(self, audio_source):
        self.dg_connection = self.deepgram.transcription.live(
            {"smart_format": True, "interim_results": True}
        )
        self.dg_connection.on("transcriptReceived", self._handle_transcript_received)
        self.dg_connection.on("error", self._handle_error)

        async for chunk in audio_source:
            await self.dg_connection.send(chunk)

        await self.dg_connection.finish()
