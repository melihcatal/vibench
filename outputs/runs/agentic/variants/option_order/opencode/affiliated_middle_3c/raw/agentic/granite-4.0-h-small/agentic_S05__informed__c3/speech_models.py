import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Google Cloud Speech-to-Text model selection utilities
# provider: Cloud Speech-to-Text streaming (service=Cloud Speech streaming)


class SpeechModels:
    """Helper to manage model configurations for Cloud Speech-to-Text.

    Example:
        model = SpeechModels.get_model(language='en-US', enable_punctuation=True)
    """

    @staticmethod
    def get_model(
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        model: str = None,
    ) -> speech.RecognitionConfig:
        """
        Return a RecognitionConfig tailored for the given parameters.
        """
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )
        if model:
            config.model = model  # e.g., "default", "phone_call", "video"
        return config

    @staticmethod
    def list_available_models() -> list:
        """
        List supported model identifiers (non-exhaustive). In practice you would query the provider API.
        """
        # Placeholder list; real implementation would query provider metadata
        return ["default", "phone_call", "video", "command_and_search"]


if __name__ == "__main__":
    print(SpeechModels.list_available_models())
