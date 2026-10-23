import asyncio
import wave
import aiofiles
from deepgram import primitives, Client

# Deepgram Streaming API
# provider: Deepgram Streaming API


async def read_audio_chunks(file_path: str, chunk_size: int = 4096):
    """Generate audio chunks from a WAV file asynchronously."""
    async with aiofiles.open(file_path, mode="rb") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk


class StreamChunks:
    """Stream audio chunks to Deepgram and receive streaming transcriptions.

    Configuration:
        DEEPGRAM_API_KEY must be set in the environment.
    """

    def __init__(
        self,
        model: str = "noble",
        punctuate: bool = True,
        profanity_filter: bool = False,
    ):
        self.client = Client()
        self.model = model
        self.punctuate = punctuate
        self.profanity_filter = profanity_filter
        # set API key from environment
        self.client.set_api_key(primitives.ApiKey.from_env("DEEPGRAM_API_KEY"))

    async def start_stream(self, audio_path: str):
        """Start streaming audio chunks to Deepgram and yield interim results."""
        async for chunk in read_audio_chunks(audio_path):
            response = await self.client.speech.recognize_stream(
                audio=chunk,
                model=self.model,
                punctuate=self.punctuate,
                profanity_filter=self.profanity_filter,
            )
            if response.type == "interim":
                yield response.interim_transcript
            elif response.type == "final":
                yield response.final_transcript


if __name__ == "__main__":
    source_path = "sample.wav"  # replace with your audio file
    streamer = StreamChunks()
    asyncio.run(streamer.start_stream(source_path))
