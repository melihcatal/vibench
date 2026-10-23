import asyncio
import os
from google.cloud import speech

async def stream_chunks():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    async def callback(response):
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

    async with client.streaming_recognize(streaming_config, callback) as stream:
        while True:
            try:
                audio_content = await asyncio.to_thread(input)
                await stream.send_audio(audio_content)
            except KeyboardInterrupt:
                break
    await stream.finish()