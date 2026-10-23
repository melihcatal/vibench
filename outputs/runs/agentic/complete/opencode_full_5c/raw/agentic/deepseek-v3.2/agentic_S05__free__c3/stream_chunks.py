import asyncio
import aiohttp
from google.cloud import speech_v1p1beta1 as speech


class AsyncAudioChunkStreamer:
    def __init__(self, client=None):
        self.client = client or speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True,
        )

    async def stream_from_async_source(self, audio_source_url, chunk_size=4096):
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_source_url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch audio from {audio_source_url}")

                buffer = bytearray()
                async for chunk in response.content.iter_chunked(chunk_size):
                    buffer.extend(chunk)

                    if len(buffer) >= chunk_size:
                        yield buffer[:chunk_size]
                        buffer = buffer[chunk_size:]

                if buffer:
                    yield buffer

    async def recognize_stream(self, audio_source_url):
        stream_generator = self.stream_from_async_source(audio_source_url)

        async def request_generator():
            async for audio_chunk in stream_generator:
                yield speech.StreamingRecognizeRequest(audio_content=bytes(audio_chunk))

        requests = request_generator()

        responses = await asyncio.to_thread(
            lambda: list(
                self.client.streaming_recognize(self.streaming_config, requests)
            )
        )

        for response in responses:
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


def stream_audio_chunks(audio_source_url, client=None):
    streamer = AsyncAudioChunkStreamer(client)

    async def run_stream():
        async for result in streamer.recognize_stream(audio_source_url):
            yield result

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        for result in loop.run_until_complete(run_stream()):
            yield result
    finally:
        loop.close()
