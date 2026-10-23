# [SAME-SCENARIO] stream_with_language.py
"""Start a streaming recognizer with language and punctuation customization."""

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

CONFIG = {
    "language_code": "es-ES",  # Spanish (Spain)
    "punctuation": True,  # Enable automatic punctuation
    "profanity_filter": False,  # Disable profanity filter
    "enable_word_time_offsets": True,  # Get word timestamps
}


async def start_streaming(language_code: str = None, enable_punctuation: bool = None):
    """Create a streaming recognizer with optional overrides."""
    client = get_speech_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code or CONFIG["language_code"],
            enable_automatic_punctuation=enable_punctuation
            if enable_punctuation is not None
            else CONFIG["punctuation"],
            enable_word_time_offsets=True,
        ),
        interim_results=True,
    )
    # Placeholder for actual audio source (e.g., microphone, file)
    # async for transcript in your_audio_source(config):
    #     process(transcript)
    print("Streaming with language:", config.config.language_code)


if __name__ == "__main__":
    # Example: start with French and disable punctuation
    asyncio.run(start_streaming(language_code="fr-FR", enable_punctuation=False))
