import asyncio
import aiohttp
from google.cloud import speech


class AsyncAudioChunkStream:
    def __init__(self, chunk_size=4096):
        self.chunk_size = chunk_size
        self.client = speech.SpeechClient()

    async def stream_from_url(self, audio_url):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="latest_long",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as response:
                async for chunk in response.content.iter_chunked(self.chunk_size):
                    if chunk:
                        request = speech.StreamingRecognizeRequest(audio_content=chunk)
                        yield request

    async def stream_from_generator(self, audio_generator):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="latest_long",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        async for chunk in audio_generator:
            if chunk:
                request = speech.StreamingRecognizeRequest(audio_content=chunk)
                yield request

    async def transcribe_stream(self, request_stream):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="latest_long",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        responses = self.client.streaming_recognize(streaming_config, request_stream)

        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                is_final = result.is_final

                yield {
                    "transcript": transcript,
                    "is_final": is_final,
                    "confidence": result.alternatives[0].confidence,
                    "language_code": "en-US",
                }


async def example_audio_generator():
    import wave
    import numpy as np

    with wave.open("example.wav", "rb") as wav_file:
        n_channels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

        chunk_size = 1024
        for i in range(0, n_frames, chunk_size):
            frames = wav_file.readframes(chunk_size)
            if not frames:
                break
            yield frames
            await asyncio.sleep(0.01)


async def main():
    streamer = AsyncAudioChunkStream()

    async for request in streamer.stream_from_generator(example_audio_generator()):
        print(f"Sent chunk of size: {len(request.audio_content)}")

    async for result in streamer.transcribe_stream(
        streamer.stream_from_generator(example_audio_generator())
    ):
        prefix = "FINAL" if result["is_final"] else "INTERIM"
        print(f"{prefix}: {result['transcript']}")


if __name__ == "__main__":
    asyncio.run(main())
