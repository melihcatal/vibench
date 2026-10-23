import os
from google.cloud import speech_v1p1beta1 as speech


async def stream_chunks():
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    client = speech.SpeechClient()

    async with speech.AsyncMicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = await client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print(result.alternatives[0].transcript)
