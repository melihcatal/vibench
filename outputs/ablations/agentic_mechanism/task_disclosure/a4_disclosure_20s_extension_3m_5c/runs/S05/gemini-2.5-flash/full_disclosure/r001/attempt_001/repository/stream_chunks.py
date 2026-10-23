import asyncio
from google.cloud import speech

async def stream_audio_chunks(audio_source, sample_rate_hertz, language_code):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text API.
    """
    # The first request contains the speech configuration, followed by the audio data.
    yield speech.StreamingRecognizeRequest(
        streaming_config=speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate_hertz,
                language_code=language_code,
            ),
            interim_results=True,
        )
    )

    async for chunk in audio_source:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

