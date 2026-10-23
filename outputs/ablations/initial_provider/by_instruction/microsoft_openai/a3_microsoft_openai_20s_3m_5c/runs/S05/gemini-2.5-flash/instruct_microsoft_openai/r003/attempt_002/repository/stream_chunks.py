import os
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

async def stream_audio_chunks(audio_chunks_async_generator):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = client.streaming_recognize(request_generator())

        async for response in responses:
            for result in response.results:
                if result.is_final:
                    print(f"Final transcript: {result.alternatives[0].transcript}")
                else:
                    print(f"Partial transcript: {result.alternatives[0].transcript}")
    except GoogleAPIError as e:
        print(f"Google Cloud Speech-to-Text API Error: {e}")
