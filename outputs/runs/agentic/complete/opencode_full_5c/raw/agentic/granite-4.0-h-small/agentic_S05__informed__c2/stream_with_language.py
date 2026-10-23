import asyncio


async def stream_with_language():
    """Starts a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text."""
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-ES",  # Spanish (Spain) example
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    # Placeholder for async audio stream source
    audio_stream = asyncio.Queue()
    # Producer (e.g., microphone) would put audio chunks into audio_stream
    # Consumer sends them to the service
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_stream
    )
    responses = client.streaming_recognize(
        streaming_config=streaming_config, requests=requests
    )
    async for response in responses:
        for result in response.results:
            print(result.alternatives[0].transcript)


# Example: asyncio.run(async for txt in stream_with_language(): print(txt))
