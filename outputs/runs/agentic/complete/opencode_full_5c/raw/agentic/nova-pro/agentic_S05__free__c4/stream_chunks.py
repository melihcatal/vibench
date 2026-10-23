import asyncio
from speech_client import create_streaming_recognizer


async def stream_chunks():
    client, streaming_config = create_streaming_recognizer()
    async for audio_data in get_audio_chunks():
        audio = types.RecognitionAudio(content=audio_data)
        request = types.StreamingRecognizeRequest(audio_content=audio.content)
        responses = client.streaming_recognize(streaming_config, [request])
        for response in responses:
            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))


async def get_audio_chunks():
    # Simulate async audio source
    for _ in range(10):
        await asyncio.sleep(1)
        yield b"simulated_audio_data"
