from google.cloud import speech_v1p1beta1 as speech
import asyncio


async def stream_audio_chunks(audio_source):
    """Streams audio chunks from an async source and yields interim transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="latest_long",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in audio_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = await client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        for result in response.results:
            yield {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
            }
