from google.cloud import speech
import asyncio

async def start_streaming_recognizer(
    audio_chunks,
    sampling_rate: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """Starts a streaming recognizer with language and punctuation settings."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in audio_chunks:
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        yield result.alternatives[0].transcript
