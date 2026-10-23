import asyncio
from google.cloud import speech_v1p1beta1 as speech

async def stream_audio_chunks(audio_source):
    """
    Streams audio chunks from an asynchronous source to Google Cloud Speech-to-Text.

    Args:
        audio_source: An asynchronous generator or iterable that yields raw audio bytes.
                      For example, an async function reading from a microphone or a file.
    """
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # An async generator that yields StreamingRecognizeRequest objects
    async def request_generator():
        # The first request must contain the streaming configuration
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)

        async for chunk in audio_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=streaming_config, requests=request_generator())

    async for response in responses:
        # Process the streaming recognition response
        # For example, print interim and final transcripts
        for result in response.results:
            if result.is_final:
                print(f"Final transcript: {result.alternatives[0].transcript}")
            else:
                print(f"Interim transcript: {result.alternatives[0].transcript}")

