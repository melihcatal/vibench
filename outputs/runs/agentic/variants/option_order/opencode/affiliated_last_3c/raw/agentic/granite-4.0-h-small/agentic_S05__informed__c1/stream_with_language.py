import asyncio
import google.cloud.speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Provider: Google Cloud Speech-to-Text Streaming
# Requires GOOGLE_APPLICATION_CREDENTIALS pointing to a service account JSON


async def stream_with_language(
    source_url: str,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """Starts a streaming recognizer with specific language and punctuation settings using Google Cloud Speech API."""
    client = speech.SpeechClient()
    # Prepare streaming config
    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        # Force model to short-lived streaming (default in v1p1beta1)
        model="default",
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    # Open audio source (placeholder URL)
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch audio source: {resp.status}")
            audio_stream = resp.content
            # Prepare request stream
            requests = [
                speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in chunk_generator(audio_stream)
            ]
            # Start streaming request
            responses = client.streaming_recognize(streaming_config, requests)
            async for response in responses:
                for result in response.results:
                    alternative = result.alternatives[0]
                    transcript = alternative.transcript
                    is_final = result.is_final
                    print(f"Transcript: {transcript} (final={is_final})")


def chunk_generator(audio_stream):
    """Yields audio chunks of reasonable size for streaming."""
    chunk_size = 32768
    remaining = audio_stream.read(chunk_size)
    while remaining:
        yield remaining
        remaining = audio_stream.read(chunk_size)


if __name__ == "__main__":
    # Example: streaming from a pre-signed Cloud Storage URL
    audio_source = "gs://my-bucket/audio.raw"
    asyncio.run(
        stream_with_language(
            audio_source, language_code="fr-FR", enable_automatic_punctuation=True
        )
    )
