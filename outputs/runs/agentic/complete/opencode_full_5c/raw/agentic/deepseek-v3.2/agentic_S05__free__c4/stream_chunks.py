import asyncio
import aiohttp
from google.cloud import speech_v1p1beta1 as speech


class AsyncAudioStreamer:
    def __init__(self, audio_source_url=None):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="latest_long",
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True,
        )
        self.audio_source_url = audio_source_url

    async def stream_from_url(self, chunk_size=4096):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.audio_source_url) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
                    yield chunk

    async def stream_from_async_generator(self, async_gen):
        async for chunk in async_gen:
            yield chunk

    def create_streaming_requests(self, audio_chunks):
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    async def recognize_stream(self, audio_chunks):
        requests = self.create_streaming_requests(audio_chunks)

        def sync_recognize():
            return self.client.streaming_recognize(
                config=self.streaming_config,
                requests=requests,
            )

        loop = asyncio.get_event_loop()
        responses = await loop.run_in_executor(None, sync_recognize)

        async for response in self._async_response_generator(responses):
            yield response

    async def _async_response_generator(self, responses):
        for response in responses:
            yield response

    async def process_audio_stream(self, stream_source):
        async for chunk in stream_source:
            request = speech.StreamingRecognizeRequest(audio_content=chunk)
            yield request
