import asyncio
from speech_client import SpeechClient
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult

# Google Cloud Speech-to-Text uses the `google.cloud.speech` SDK
# and `speech.SpeechClient` for its operations.


async def stream_audio_chunks(audio_chunk_source, sample_rate: int = 16000):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text.

    Args:
        audio_chunk_source: An async iterable that yields audio chunks (bytes).
        sample_rate: The sample rate of the audio chunks.

    Yields:
        SpeechRecognitionResult: Interim or final transcription results.
    """
    config_params = StreamingRecognitionConfig(
        sample_rate_hertz=sample_rate, language_code="en-US", interim_results=True
    )
    speech_client = SpeechClient()

    try:
        async for response in speech_client.stream_audio_to_text(
            audio_chunk_source, config_params
        ):
            for result in response.results:
                yield SpeechRecognitionResult(
                    transcript=result.alternatives[0].transcript,
                    is_final=result.is_final,
                    confidence=result.alternatives[0].confidence,
                )
    except Exception as e:
        print(f"Error during audio chunk streaming: {e}")
        raise
