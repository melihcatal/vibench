import asyncio
import queue
import threading
from google.cloud import speech


class AsyncAudioChunkStream:
    def __init__(self, chunk_queue=None):
        self.chunk_queue = chunk_queue or asyncio.Queue()
        self.client = speech.SpeechClient()

    async def stream_audio_chunks(self, audio_chunks_iterator):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        async def request_generator():
            async for chunk in audio_chunks_iterator:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        responses = await self.client.streaming_recognize(
            config=streaming_config,
            requests=request_generator(),
        )

        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                is_final = result.is_final

                await self.chunk_queue.put((transcript, is_final))

                if is_final:
                    yield transcript, True
                else:
                    yield transcript, False


class AudioChunkProducer:
    def __init__(self, source_callback, chunk_size=1024):
        self.source_callback = source_callback
        self.chunk_size = chunk_size
        self.running = False

    async def produce_chunks(self):
        self.running = True
        while self.running:
            chunk = await self.source_callback()
            if chunk is None:
                break
            yield chunk

    def stop(self):
        self.running = False


def stream_from_async_source(source_callback):
    producer = AudioChunkProducer(source_callback)
    streamer = AsyncAudioChunkStream()

    async def stream_wrapper():
        async for transcript, is_final in streamer.stream_audio_chunks(
            producer.produce_chunks()
        ):
            yield transcript, is_final

    return stream_wrapper()
