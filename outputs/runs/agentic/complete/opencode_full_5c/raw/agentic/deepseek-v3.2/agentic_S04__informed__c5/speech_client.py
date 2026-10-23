import os
import assemblyai as aai


def get_speech_client() -> aai.Transcript:
    """Initialize and return AssemblyAI speech client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key
    return aai.Transcript


def validate_audio_url(audio_url: str) -> bool:
    """Validate audio URL format."""
    return audio_url.startswith(("http://", "https://", "s3://", "gs://"))


def get_default_config() -> dict:
    """Get default transcription configuration."""
    return {
        "language_code": "en",
        "speech_model": "best",
        "speaker_labels": False,
        "word_boost": [],
        "filter_profanity": False,
    }
