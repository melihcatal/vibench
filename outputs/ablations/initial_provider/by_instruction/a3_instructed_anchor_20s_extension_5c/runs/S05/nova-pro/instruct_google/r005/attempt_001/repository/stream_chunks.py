import asyncio
from google.cloud import speech
from speech_client import create_speech_client
from speech_models import StreamingRecognizeRequest


async def stream_chunks():
    client = create_speech_client()
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = speech.types.StreamingRecognitionConfig(config=config, interim_results=True)

    async with client:
        requests = (StreamingRecognizeRequest(audio_content=content)
                    for content in async_audio_generator())
        responses = client.streaming_recognize(streaming_config, requests)

        async for response in responses:
            for result in response.results:
                print(u'Transcript: {}'.format(result.alternatives[0].transcript))

async def async_audio_generator():
    # Implement async audio generator
    yield b'audio_chunk_1'
    yield b'audio_chunk_2'

if __name__ == '__main__':
    asyncio.run(stream_chunks())