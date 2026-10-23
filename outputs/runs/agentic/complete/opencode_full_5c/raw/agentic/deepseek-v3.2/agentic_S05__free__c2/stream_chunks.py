import asyncio
import aiohttp
import io
from google.cloud import speech_v1p1beta1 as speech


class AsyncAudioChunkStream:
    def __init__(self, audio_source_url, chunk_size=4096):
        self.audio_source_url = audio_source_url
        self.chunk_size = chunk_size
        self.client = speech.SpeechClient()

    async def stream_audio_chunks(self):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(self.audio_source_url) as response:
                audio_buffer = io.BytesIO()

                async for chunk in response.content.iter_chunked(self.chunk_size):
                    audio_buffer.write(chunk)

                    if audio_buffer.tell() >= self.chunk_size:
                        audio_data = audio_buffer.getvalue()
                        audio_buffer = io.BytesIO()

                        request = speech.StreamingRecognizeRequest(
                            audio_content=audio_data
                        )

                        responses = self.client.streaming_recognize(
                            streaming_config,
                            [request],
                        )

                        for response in responses:
                            if response.results:
                                yield response

                if audio_buffer.tell() > 0:
                    audio_data = audio_buffer.getvalue()
                    request = speech.StreamingRecognizeRequest(audio_content=audio_data)

                    responses = self.client.streaming_recognize(
                        streaming_config,
                        [request],
                    )

                    for response in responses:
                        if response.results:
                            yield response


async def process_streaming_chunks(audio_url):
    streamer = AsyncAudioChunkStream(audio_url)

    async for response in streamer.stream_audio_chunks():
        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            is_final = result.is_final

            yield {
                "transcript": transcript,
                "is_final": is_final,
                "result": result,
            }


def stream_from_async_source(audio_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        results = []
        async for chunk_result in process_streaming_chunks(audio_url):
            results.append(chunk_result)
        return results

    return loop.run_until_complete(run())


if __name__ == "__main__":
    test_url = (
        "https://storage.googleapis.com/cloud-samples-data/speech/brooklyn_bridge.raw"
    )
    for chunk in stream_from_async_source(test_url):
        status = "FINAL" if chunk["is_final"] else "INTERIM"
        print(f"[{status}] {chunk['transcript']}")
