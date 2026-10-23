import asyncio
from google.cloud import speech_v1 as speech

# Streams audio chunks from an async generator and sends them to Google Cloud Speech-to-Text streaming.
# Provider: Google Cloud Speech (service=Cloud Speech streaming)


async def stream_audio_chunks(chunks, config, **kwargs):
    """Yield StreamingRecognizeRequests for each audio chunk.

    chunks: async iterable yielding bytes of audio data
    config: RecognitionConfig instance
    """
    client = speech.v1.SpeechClient()
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    async for audio in chunks:
        yield request.replace(audio_stream=audio)
