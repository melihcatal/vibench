import os
from typing import Optional
import google.cloud.speech as speech


def get_speech_client() -> speech.SpeechClient:
    """Initialize and return Google Cloud Speech client."""
    client = speech.SpeechClient()
    return client


def load_audio_config(
    encoding: str = "LINEAR16",
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: Optional[str] = None,
    use_enhanced: bool = False,
) -> speech.RecognitionConfig:
    """Create audio recognition configuration."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        use_enhanced=use_enhanced,
    )

    if model:
        config.model = model

    return config


def create_streaming_config(
    config: speech.RecognitionConfig,
    interim_results: bool = True,
    single_utterance: bool = False,
    enable_word_time_offsets: bool = False,
    profanity_filter: bool = False,
) -> speech.StreamingRecognitionConfig:
    """Create streaming recognition configuration."""
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
        single_utterance=single_utterance,
    )

    if enable_word_time_offsets:
        streaming_config.config.enable_word_time_offsets = True

    if profanity_filter:
        streaming_config.config.profanity_filter = profanity_filter

    return streaming_config


def get_audio_encoding(encoding_str: str) -> speech.RecognitionConfig.AudioEncoding:
    """Convert encoding string to Speech enum."""
    encoding_map = {
        "LINEAR16": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "FLAC": speech.RecognitionConfig.AudioEncoding.FLAC,
        "MULAW": speech.RecognitionConfig.AudioEncoding.MULAW,
        "AMR": speech.RecognitionConfig.AudioEncoding.AMR,
        "AMR_WB": speech.RecognitionConfig.AudioEncoding.AMR_WB,
        "OGG_OPUS": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "SPEEX_WITH_HEADER_BYTE": speech.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE,
    }

    return encoding_map.get(
        encoding_str, speech.RecognitionConfig.AudioEncoding.LINEAR16
    )


def validate_environment():
    """Validate required environment variables are set."""
    required_vars = ["GOOGLE_APPLICATION_CREDENTIALS"]
    missing = []

    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please set GOOGLE_APPLICATION_CREDENTIALS to path of service account key file."
        )


class SpeechClientWrapper:
    """Wrapper for Google Cloud Speech client with convenience methods."""

    def __init__(self):
        validate_environment()
        self.client = get_speech_client()

    def recognize_audio_file(
        self, audio_file_path: str, config: speech.RecognitionConfig
    ) -> speech.RecognizeResponse:
        """Recognize speech from an audio file."""
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        response = self.client.recognize(config=config, audio=audio)
        return response

    def streaming_recognize(
        self, streaming_config: speech.StreamingRecognitionConfig, audio_generator
    ) -> speech.SpeechClient.streaming_recognize:
        """Perform streaming recognition."""
        return self.client.streaming_recognize(streaming_config, audio_generator)
